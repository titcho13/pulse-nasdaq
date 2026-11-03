import pandas as pd
import numpy as np
import yfinance as yf

SYMBOLE = "NQ=F"

SEUIL_15M = 2.0
SEUIL_5M = 1.5


def get_signal():

    df5 = yf.download(
        SYMBOLE,
        period="20d",
        interval="5m",
        progress=False
    )

    if isinstance(df5.columns, pd.MultiIndex):
        df5.columns = df5.columns.get_level_values(0)

    df5 = df5.rename(columns=str.lower)

    df15 = df5.resample("15min").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    }).dropna()

    # --------- SIGNAL 15M ---------

    df15["ret"] = df15["close"].pct_change()

    scale15 = (
        1.4826
        * df15["ret"].abs().rolling(100).median()
    )

    df15["z"] = df15["ret"] / scale15

    dernier15 = df15.iloc[-1]

    sens15 = 0

    if dernier15["z"] >= SEUIL_15M:
        sens15 = 1

    elif dernier15["z"] <= -SEUIL_15M:
        sens15 = -1

    # --------- VALIDATION 5M ---------

    df5["ret"] = df5["close"].pct_change()

    scale5 = (
        1.4826
        * df5["ret"].abs().rolling(200).median()
    )

    df5["z"] = df5["ret"] / scale5

    derniere5 = df5.iloc[-1]

    valid5 = False

    if sens15 == 1 and derniere5["z"] >= SEUIL_5M:
        valid5 = True

    if sens15 == -1 and derniere5["z"] <= -SEUIL_5M:
        valid5 = True

    # --------- ETAT ---------

    if sens15 == 1:
        signal = "ACHAT PRIORITAIRE"

    elif sens15 == -1:
        signal = "VENTE PRIORITAIRE"

    else:
        signal = "AUCUN SIGNAL"

    if valid5:

        force = abs(float(derniere5["z"]))

        if force >= 3:
            qualite = "PREMIUM"

        elif force >= 2:
            qualite = "NORMAL"

        else:
            qualite = "TARDIF"

    else:

        if sens15 != 0:
            qualite = "EN ATTENTE"
        else:
            qualite = "-"

    return {
        "signal": signal,
        "qualite": qualite,
        "prix": round(float(df5["close"].iloc[-1]), 2),
        "z15": round(float(dernier15["z"]), 2),
        "z5": round(float(derniere5["z"]), 2)
    }
