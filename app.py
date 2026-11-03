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
qualite = data["qualite"]
prix = data["prix"]
z15 = data["z15"]
z5 = data["z5"]
score = data["score"]

# =====================
# TITRE
# =====================

st.title("📈 PULSE NASDAQ")

# =====================
# SIGNAL PRINCIPAL
# =====================

if signal == "ACHAT PRIORITAIRE":

    st.success("🟢 ACHAT PRIORITAIRE")

elif signal == "VENTE PRIORITAIRE":

    st.error("🔴 VENTE PRIORITAIRE")

elif z15 > 1:

    st.warning("🟠 SURVEILLANCE ACHAT")

elif z15 < -1:

    st.warning("🟠 SURVEILLANCE VENTE")

else:

    st.info("⚪ MARCHÉ NEUTRE")

# =====================
# KPIs
# =====================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Qualité",
        qualite
    )

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

# =====================
# SCORE
# =====================

st.subheader("Force du signal")

st.progress(score / 100)

if score >= 85:

    st.success("🔥 SIGNAL EXCEPTIONNEL")

elif score >= 70:

    st.success("✅ SIGNAL FORT")

elif score >= 50:

    st.warning("⚠️ SIGNAL NORMAL")

else:

    st.error("❌ SIGNAL FAIBLE")

# =====================
# VALIDATION
# =====================

st.divider()

st.subheader("Validation 15 min → 5 min")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Z-Score 15 min",
        z15
    )

with c2:
    st.metric(
        "Z-Score 5 min",
        z5
    )

# =====================
# CHECKLIST SETUP
# =====================

st.divider()

st.subheader("🎯 État du setup")

critere_z15_achat = z15 >= 2
critere_z15_vente = z15 <= -2

critere_z5_achat = z5 >= 1.5
critere_z5_vente = z5 <= -1.5

if signal == "ACHAT PRIORITAIRE" or z15 > 0:

    st.write(
        f"{'✅' if critere_z15_achat else '⬜'} Z15 > 2"
    )

    st.write(
        f"{'✅' if critere_z5_achat else '⬜'} Z5 > 1.5"
    )

else:

    st.write(
        f"{'✅' if critere_z15_vente else '⬜'} Z15 < -2"
    )

    st.write(
        f"{'✅' if critere_z5_vente else '⬜'} Z5 < -1.5"
    )

# =====================
# CE QUI ME FERA ACHETER
# =====================

st.divider()

st.subheader("🟢 Ce qui me fera acheter")

if critere_z15_achat:
    st.success("✅ Impulsion 15 min validée")
else:
    st.warning(
        f"Manque encore {round(2-z15,2)} de Z15"
    )

if critere_z5_achat:
    st.success("✅ Confirmation 5 min validée")
else:
    st.warning(
        f"Manque encore {round(1.5-z5,2)} de Z5"
    )

# =====================
# CE QUI ME FERA VENDRE
# =====================

st.divider()

st.subheader("🔴 Ce qui me fera vendre")

if critere_z15_vente:
    st.success("✅ Impulsion baissière 15 min validée")
else:
    st.warning(
        f"Manque encore {round(abs(-2-z15),2)}"
    )

if critere_z5_vente:
    st.success("✅ Confirmation baissière 5 min validée")
else:
    st.warning(
        f"Manque encore {round(abs(-1.5-z5),2)}"
    )

# =====================
# DIAGNOSTIC
# =====================

st.divider()

st.subheader("Diagnostic")

if signal == "ACHAT PRIORITAIRE":

    st.success(
        "Les conditions d'achat sont réunies."
    )

elif signal == "VENTE PRIORITAIRE":

    st.error(
        "Les conditions de vente sont réunies."
    )

elif abs(z15) > 1:

    st.warning(
        "Le marché entre dans une zone de surveillance."
    )

else:

    st.info(
        "Aucune anomalie significative détectée."
    )

# =====================
# DONNÉES
# =====================

st.divider()

with st.expander("Données techniques"):

    st.json(data)

# =====================
# PIED DE PAGE
# =====================

st.divider()

st.caption(
    f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
)
