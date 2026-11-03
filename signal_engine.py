import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

st.set_page_config(
    page_title="PULSE NASDAQ",
    page_icon="📈",
    layout="wide"
)

SYMBOLE = "NQ=F"

@st.cache_data(ttl=60)
def charger_donnees():
    df = yf.download(
        SYMBOLE,
        period="30d",
        interval="5m",
        progress=False
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df

def calcul_signaux(df):

    df = df.copy()

    df["ret"] = df["Close"].pct_change()

    vol_med = df["Volume"].rolling(50).median()

    df["ratio_vol"] = df["Volume"] / vol_med

    df["ema20"] = df["Close"].ewm(span=20).mean()
    df["ema50"] = df["Close"].ewm(span=50).mean()

    df["momentum"] = df["Close"].pct_change(3)

    dernier = df.iloc[-1]

    signal = "NEUTRE"

    if (
        dernier["ema20"] > dernier["ema50"]
        and dernier["momentum"] > 0
        and dernier["ratio_vol"] > 1.3
    ):
        signal = "ACHAT"

    elif (
        dernier["ema20"] < dernier["ema50"]
        and dernier["momentum"] < 0
        and dernier["ratio_vol"] > 1.3
    ):
        signal = "VENTE"

    score = 0

    score += min(abs(dernier["momentum"]) * 1000, 40)
    score += min(dernier["ratio_vol"] * 10, 30)

    if signal == "ACHAT":
        score += 30

    elif signal == "VENTE":
        score += 30

    score = min(round(score), 100)

    return signal, score

df = charger_donnees()

signal, score = calcul_signaux(df)

st.title("📈 PULSE NASDAQ")

col1, col2, col3 = st.columns(3)

with col1:

    if signal == "ACHAT":
        st.success("🟢 ACHAT")

    elif signal == "VENTE":
        st.error("🔴 VENTE")

    else:
        st.warning("🟡 NEUTRE")

with col2:

    st.metric(
        "Score PULSE",
        f"{score}/100"
    )

with col3:

    prix = round(df["Close"].iloc[-1], 2)

    st.metric(
        "Dernier prix",
        prix
    )

st.progress(score / 100)

if score >= 85:
    st.success("🔥 SIGNAL EXCEPTIONNEL")

elif score >= 70:
    st.info("✅ SIGNAL FORT")

elif score >= 50:
    st.warning("⚠️ SIGNAL NORMAL")

else:
    st.error("❌ SIGNAL FAIBLE")

st.subheader("Nasdaq Future")

st.line_chart(df["Close"])

st.subheader("Dernières données")

st.dataframe(
    df.tail(20),
    use_container_width=True
)

st.caption(
    f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
)
