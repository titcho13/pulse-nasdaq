import streamlit as st
from datetime import datetime
from signal_engine import get_signal

st.set_page_config(
    page_title="Pulse Nasdaq",
    page_icon="📈",
    layout="wide"
)

# =====================
# DONNÉES
# =====================

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

    st.success(f"🟢 {signal}")

elif signal == "VENTE PRIORITAIRE":

    st.error(f"🔴 {signal}")

else:

    st.warning("🟡 AUCUN SIGNAL")

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
# BARRE DE FORCE
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
# INTERPRÉTATION
# =====================

st.divider()

st.subheader("Diagnostic")

if signal == "ACHAT PRIORITAIRE":

    st.success(
        "Le moteur détecte un contexte acheteur."
    )

elif signal == "VENTE PRIORITAIRE":

    st.error(
        "Le moteur détecte un contexte vendeur."
    )

else:

    st.info(
        "Aucune anomalie significative détectée."
    )

# =====================
# QUALITÉ
# =====================

if qualite == "PREMIUM":

    st.success(
        "🔥 Validation rapide du signal 15 min par le 5 min."
    )

elif qualite == "NORMAL":

    st.info(
        "✅ Signal validé mais avec une puissance modérée."
    )

elif qualite == "TARDIF":

    st.warning(
        "⚠️ Validation tardive."
    )

elif qualite == "EN ATTENTE":

    st.warning(
        "⏳ Signal 15 min détecté mais pas encore validé par le 5 min."
    )

# =====================
# DONNÉES TECHNIQUES
# =====================

st.divider()

with st.expander("Données techniques"):

    st.write({
        "Signal": signal,
        "Qualité": qualite,
        "Prix": prix,
        "Z15": z15,
        "Z5": z5,
        "Score": score
    })

# =====================
# PIED DE PAGE
# =====================

st.divider()

st.caption(
    f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
)
