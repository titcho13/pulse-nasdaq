import streamlit as st
from datetime import datetime
from signal_engine import get_signal

st.set_page_config(
    page_title="Pulse Nasdaq",
    page_icon="📈",
    layout="wide"
)

data = get_signal()

signal = data["signal"]
prix = data["prix"]
score = data["score"]

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
        "Prix Nasdaq",
        prix
    )

with col3:
    st.metric(
        "Score Pulse",
        f"{score}/100"
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

st.subheader("Analyse")

st.write(f"Signal actuel : **{signal}**")
st.write(f"Prix actuel : **{prix}**")
st.write(f"Force du signal : **{score}/100**")

st.divider()

st.caption(
    f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
)
