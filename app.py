import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from signal_engine import get_signal

# =====================
# CONFIGURATION
# =====================

st.set_page_config(
    page_title="Pulse Nasdaq",
    page_icon="📈",
    layout="wide"
)


# =====================
# RAFRAÎCHISSEMENT
# =====================

st_autorefresh(
    interval=15000,
    key="pulse_refresh"
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
chrono = data["chrono"]
expire = data["expire"]

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

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Qualité", qualite)

with col2:
    st.metric("Prix Nasdaq", prix)

with col3:
    st.metric("Score Pulse", f"{score}/100")

with col4:
    st.metric("Chrono", chrono)

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

if signal != "AUCUN SIGNAL":

    if expire:

        st.error(
            "⛔ Délai de validation dépassé"
        )

    else:

        st.warning(
            f"⏳ Temps restant : {chrono}"
        )

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
# CHECKLIST
# =====================

st.divider()

st.subheader("🎯 État du setup")

achat15 = z15 >= 2
achat5 = z5 >= 1.5

vente15 = z15 <= -2
vente5 = z5 <= -1.5

if signal == "ACHAT PRIORITAIRE" or z15 > 0:

    st.write(
        f"{'✅' if achat15 else '⬜'} Impulsion 15 min"
    )

    st.write(
        f"{'✅' if achat5 else '⬜'} Confirmation 5 min"
    )

else:

    st.write(
        f"{'✅' if vente15 else '⬜'} Impulsion 15 min"
    )

    st.write(
        f"{'✅' if vente5 else '⬜'} Confirmation 5 min"
    )

# =====================
# CE QUI ME FERA ACHETER
# =====================

st.divider()

st.subheader("🟢 Ce qui me fera acheter")

st.write(
    f"{'✅' if achat15 else '⬜'} Z15 > 2"
)

st.write(
    f"{'✅' if achat5 else '⬜'} Z5 > 1.5"
)

# =====================
# CE QUI ME FERA VENDRE
# =====================

st.divider()

st.subheader("🔴 Ce qui me fera vendre")

st.write(
    f"{'✅' if vente15 else '⬜'} Z15 < -2"
)

st.write(
    f"{'✅' if vente5 else '⬜'} Z5 < -1.5"
)

# =====================
# DIAGNOSTIC
# =====================

st.divider()

st.subheader("Diagnostic")

if signal == "ACHAT PRIORITAIRE":

    st.success(
        "Conditions acheteuses réunies."
    )

elif signal == "VENTE PRIORITAIRE":

    st.error(
        "Conditions vendeuses réunies."
    )

elif abs(z15) > 1:

    st.warning(
        "Zone de surveillance active."
    )

else:

    st.info(
        "Aucune anomalie détectée."
    )

# =====================
# DONNÉES TECHNIQUES
# =====================

st.divider()

with st.expander("Données techniques"):

    st.json(data)

# =====================
# PIED DE PAGE
# =====================

st.divider()

st.caption(
    f"Mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
)
