import streamlit as st
from datetime import datetime
from signal_engine import get_signal

st.set_page_config(
    page_title="Pulse Nasdaq",
    page_icon="📈",
    layout="wide"
)

signal, prix = get_signal()

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
        f"{prix}"
    )

with col3:
    st.metric(
        "Dernière mise à jour",
        datetime.now().strftime("%H:%M:%S")
    )

st.divider()

st.subheader("Signal actuel")

if signal == "ACHAT":
    st.success(
        "Le moteur détecte actuellement un contexte acheteur."
    )

elif signal == "VENTE":
    st.error(
        "Le moteur détecte actuellement un contexte vendeur."
    )

else:
    st.info(
        "Aucun signal exploitable."
    )

st.divider()

st.subheader("Évolution future")

st.info(
    """
    Version 2 :

    ✅ Signaux 15 min

    ✅ Confirmation 5 min

    ✅ PREMIUM

    ✅ NORMAL

    ✅ TARDIF

    ✅ Compte à rebours

    ✅ Historique SQLite

    ✅ Alertes Telegram
    """
)

st.caption(
    f"Mis à jour le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}"
)
