import pandas as pd
import yfinance as yf
import numpy as np


def get_signal():

    df = yf.download(
        "NQ=F",
        period="10d",
        interval="5m",
        progress=False
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df["ema20"] = df["Close"].ewm(span=20).mean()
    df["ema50"] = df["Close"].ewm(span=50).mean()

    df["momentum"] = df["Close"].pct_change(3)

    vol_med = df["Volume"].rolling(50).median()
    df["ratio_vol"] = df["Volume"] / vol_med

    dernier = df.iloc[-1]

    signal = "NEUTRE"

    if (
        dernier["ema20"] > dernier["ema50"]
        and dernier["momentum"] > 0
    ):
        signal = "ACHAT"

    elif (
        dernier["ema20"] < dernier["ema50"]
        and dernier["momentum"] < 0
    ):
        signal = "VENTE"

    score = 0

    score += min(abs(dernier["momentum"]) * 10000, 40)
    score += min(dernier["ratio_vol"] * 15, 30)

    if signal != "NEUTRE":
        score += 30

    score = min(int(score), 100)

    prix = round(float(dernier["Close"]), 2)

    return {
        "signal": signal,
        "prix": prix,
        "score": score
    }
