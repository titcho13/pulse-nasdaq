import pandas as pd
import yfinance as yf


def get_signal():

    df = yf.download(
        "NQ=F",
        period="5d",
        interval="5m",
        progress=False
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df["ema20"] = df["Close"].ewm(span=20).mean()
    df["ema50"] = df["Close"].ewm(span=50).mean()

    dernier = df.iloc[-1]

    if dernier["ema20"] > dernier["ema50"]:
        signal = "ACHAT"
    else:
        signal = "VENTE"

    prix = round(float(dernier["Close"]), 2)

    return signal, prix
