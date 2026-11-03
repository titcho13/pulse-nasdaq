import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Pulse Nasdaq",
    page_icon="📈",
    layout="wide"
)

st.title("📈 PULSE NASDAQ")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Signal",
        "EN ATTENTE"
    )

with col2:
    st.metric(
        "Qualité",
        "-"
    )

with col3:
    st.metric(
        "Dernière mise à jour",
        datetime.now().strftime("%H:%M")
    )

st.divider()

st.subheader("État du moteur")

st.info(
    "Le moteur de signaux Nasdaq sera connecté ici."
)

st.subheader("Historique")

st.dataframe(
    [],
    use_container_width=True
)
