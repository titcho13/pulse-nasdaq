import pandas as pd
import numpy as np
import yfinance as yf

SYMBOLE = "NQ=F"

SEUIL_15M = 2.0
SEUIL_5M = 1.5

FUSEAU = "Europe/Paris"


def telecharger_donnees():

    df = yf.download(
        SYMBOLE,
        period="20d",
        interval="5m",
        progress=False,
        auto_adjust=False
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns = [c.lower() for c in df.columns]

    return df


def construire_15m(df5):

    df15 = df5.resample(
        "15min",
        label="left",
        closed="left"
    ).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    })

    df15 = df15.dropna()

    return df15


def calcul_zscore(df, fenetre):

    df = df.copy()

    df["ret"] = df["close"].pct_change()

    scale = (
        1.4826
        * df["ret"].abs().rolling(
            fenetre,
            min_periods=50
        ).median()
    )

    df["zscore"] = df["ret"] / scale.replace(0, np.nan)

    return df


def get_signal():

    try:

        # --------------------
        # DATA
        # --------------------

        df5 = telecharger_donnees()

        df15 = construire_15m(df5)

        df5 = calcul_zscore(df5, 200)
        df15 = calcul_zscore(df15, 100)

        dernier_5m = df5.iloc[-1]
        dernier_15m = df15.iloc[-1]

        z15 = float(
            np.nan_to_num(
                dernier_15m["zscore"],
                nan=0
            )
        )

        z5 = float(
            np.nan_to_num(
                dernier_5m["zscore"],
                nan=0
            )
        )

        prix = round(
            float(dernier_5m["close"]),
            2
        )

        # --------------------
        # SIGNAL 15 MIN
        # --------------------

        sens = 0

        if z15 >= SEUIL_15M:
            sens = 1

        elif z15 <= -SEUIL_15M:
            sens = -1

        # --------------------
        # VALIDATION 5 MIN
        # --------------------

        validation = False

        if sens == 1 and z5 >= SEUIL_5M:
            validation = True

        if sens == -1 and z5 <= -SEUIL_5M:
            validation = True

        # --------------------
        # SIGNAL
        # --------------------

        if sens == 1:
            signal = "ACHAT PRIORITAIRE"

        elif sens == -1:
            signal = "VENTE PRIORITAIRE"

        else:
            signal = "AUCUN SIGNAL"

        # --------------------
        # QUALITÉ
        # --------------------

        if validation:

            force = abs(z5)

            if force >= 3:
                qualite = "PREMIUM"

            elif force >= 2:
                qualite = "NORMAL"

            else:
                qualite = "TARDIF"

        else:

            if sens != 0:
                qualite = "EN ATTENTE"
            else:
                qualite = "-"

        # --------------------
        # SCORE PULSE
        # --------------------

        score = 0

        score += min(abs(z15) * 15, 40)
        score += min(abs(z5) * 15, 40)

        if validation:
            score += 20

        score = min(
            round(score),
            100
        )

        # --------------------
        # RETOUR
        # --------------------

        return {
            "signal": signal,
            "qualite": qualite,
            "prix": prix,
            "z15": round(z15, 2),
            "z5": round(z5, 2),
            "score": score
        }

    except Exception as e:

        return {
            "signal": "ERREUR",
            "qualite": "-",
            "prix": 0,
            "z15": 0,
            "z5": 0,
            "score": 0,
            "erreur": str(e)
        }
