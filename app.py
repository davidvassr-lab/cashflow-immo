import streamlit as st

st.set_page_config(
    page_title="Calculateur Cash-Flow Immo",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ══════════════════════════════════════════
   VARIABLES — même palette que le dashboard
   ══════════════════════════════════════════ */
:root {
  --bg:        #0f1419;
  --panel:     #1a2029;
  --panel2:    #232b36;
  --border:    #2d3748;
  --text:      #e8ecef;
  --text-dim:  #8a95a5;
  --text-mute: #5a6470;
  --accent:    #4f8cff;
  --green:     #22c55e;
  --red:       #ef4444;
  --amber:     #f59e0b;
  --shadow:    0 4px 20px rgba(0,0,0,0.4);
}

/* ── Fond global ── */
html, body,
[class*="css"],
.stApp,
.block-container,
section[data-testid="stSidebar"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.block-container { padding-top: 2rem !important; max-width: 780px !important; }

/* ── Inputs Streamlit ── */
input, textarea,
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"] {
    background-color: var(--panel2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
label, .stNumberInput label, p {
    color: var(--text-dim) !important;
    font-size: 0.87rem !important;
}

/* ── Titres H1 ── */
h1 {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #4f8cff, #a855f7) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: 0.01em !important;
}

/* ── Titres H3 (sections) ── */
h3 {
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.15em !important;
    color: var(--text-dim) !important;
    margin-top: 1.8rem !important;
    margin-bottom: 0.5rem !important;
    -webkit-text-fill-color: var(--text-dim) !important;
}

hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ══════════════════════════════════════════
   KPI CARDS — style dashboard
   ══════════════════════════════════════════ */
.kpi-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 12px;
}
.kpi-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
}
.kpi-card.green::before { background: var(--green); }
.kpi-card.amber::before { background: var(--amber); }
.kpi-card.red::before   { background: var(--red); }
.kpi-card.purple::before { background: #a855f7; }

.kpi-label {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-dim);
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.1;
}
.kpi-sub {
    font-size: 0.72rem;
    color: var(--text-mute);
    margin-top: 4px;
}

/* ══════════════════════════════════════════
   BLOCS RÉCAP — style panel dashboard
   ══════════════════════════════════════════ */
.bloc {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.75rem;
    box-shadow: var(--shadow);
}
.bloc-title {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-dim);
    margin-bottom: 0.9rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.ligne {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.48rem 0;
    border-bottom: 1px solid rgba(45,55,72,0.5);
    font-size: 0.88rem;
    color: var(--text-dim);
}
.ligne:last-child { border-bottom: none; }
.ligne .val { font-weight: 600; color: var(--text); }
.ligne.total {
    font-weight: 700;
    color: var(--text);
    font-size: 0.92rem;
    padding-top: 0.7rem;
    border-top: 1px solid var(--border);
    border-bottom: none;
    margin-top: 0.2rem;
}
.ligne.total .val { color: var(--accent); font-size: 1rem; }

/* ══════════════════════════════════════════
   RÉSULTAT CASHFLOW — carte principale
   ══════════════════════════════════════════ */
.result-box {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2.2rem 1.5rem;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
}
.result-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.result-box.vert::before  { background: var(--green); }
.result-box.rouge::before { background: var(--red); }
.result-box.bleu::before  { background: var(--accent); }

.result-label {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-mute);
    margin-bottom: 0.7rem;
}
.result-value {
    font-size: 3.8rem;
    font-weight: 700;
    line-height: 1;
    color: var(--text);
}
.result-value.vert  { color: var(--green); }
.result-value.rouge { color: var(--red); }
.result-unit {
    font-size: 0.8rem;
    color: var(--text-mute);
    margin-top: 0.5rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ══════════════════════════════════════════
   MÉTRIQUES SECONDAIRES — style kpi-card
   ══════════════════════════════════════════ */
.metric-row {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.6rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    color: var(--text-dim);
    box-shadow: var(--shadow);
}
.metric-row .mval {
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text);
}
.metric-row .mval.vert  { color: var(--green); }
.metric-row .mval.rouge { color: var(--red); }

/* ══════════════════════════════════════════
   BOUTON CTA
   ══════════════════════════════════════════ */
.cta-btn {
    display: block;
    text-align: center;
    background: linear-gradient(135deg, #4f8cff, #a855f7);
    color: white !important;
    font-weight: 700;
    font-size: 0.92rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    text-decoration: none !important;
    margin-top: 2rem;
    box-shadow: 0 4px 20px rgba(79,140,255,0.3);
}

/* ── Gate email ── */
.email-wrapper { max-width: 460px; margin: 4rem auto; text-align: center; }
.legal { font-size: 0.72rem; color: var(--text-mute); margin-top: 0.8rem; }

/* ── Footer ── */
footer {
    font-size: 0.7rem;
    color: var(--text-mute);
    text-align: center;
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)

# ── Fonctions ────────────────────────────────────────────────────────────────

def mensualite(emprunt, taeg_annuel, duree_ans):
    t = taeg_annuel / 12
    n = duree_ans * 12
    if emprunt <= 0 or n == 0:
        return 0.0
    if t == 0:
        return emprunt / n
    return emprunt * t / (1 - (1 + t) ** (-n))

def capital_rembourse(emprunt, taeg_annuel, duree_ans, annee_n):
    if emprunt <= 0 or annee_n <= 0 or annee_n > duree_ans:
        return None
    t = taeg_annuel / 12
    n = duree_ans * 12
    k = annee_n * 12
    if t == 0:
        return emprunt * k / n
    M = emprunt * t / (1 - (1 + t) ** (-n))
    crd = emprunt * (1 + t) ** k - M * ((1 + t) ** k - 1) / t
    return emprunt - max(0.0, crd)

def fmt(n):
    return f"{n:,.0f} €".replace(",", "\u202f")

# ── Session state ─────────────────────────────────────────────────────────────

if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

# ── Gate email ────────────────────────────────────────────────────────────────

if not st.session_state.access_granted:
    st.markdown('<div class="email-wrapper">', unsafe_allow_html=True)
    st.markdown("## 🏠 Calculateur Cash-Flow Immo")
    st.markdown("Entrez votre email pour accéder gratuitement à l'outil :")
    with st.form("gate"):
        email = st.text_input("Email", placeholder="vous@exemple.com", label_visibility="collapsed")
        ok = st.form_submit_button("Accéder au calculateur →", use_container_width=True, type="primary")
        if ok:
            e = email.strip()
            if "@" in e and "." in e.split("@")[-1]:
                st.session_state.access_granted = True
                st.rerun()
            else:
                st.error("Email invalide.")
    st.markdown('<p class="legal">En renseignant votre email, vous acceptez d\'être recontacté.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ── Titre ─────────────────────────────────────────────────────────────────────

st.title("🏠 Calculateur Cash-Flow Immo Avant Impôt")
st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — ACQUISITION
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 1. Acquisition")

prix = st.number_input("Prix négocié FAI (€)", min_value=0, value=150000, step=1000)

frais_notaire_pct = st.number_input(
    "Frais de notaire (%)",
    min_value=0.0, max_value=20.0, value=8.5, step=0.1,
    help="8,5% par défaut — modifiable"
)
frais_notaire = round(prix * frais_notaire_pct / 100)

frais_dossier = st.number_input("Frais de dossier bancaires (€)", min_value=0, value=750, step=50)
travaux       = st.number_input("Montant des travaux (€)",         min_value=0, value=0,   step=1000)
mobilier      = st.number_input("Mobilier / Ameublement (€)",      min_value=0, value=0,   step=500)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — FINANCEMENT
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 2. Financement")

apport       = st.number_input("Apport (€)",           min_value=0, value=0,  step=1000)
duree_ans    = st.number_input("Durée d'emprunt (ans)", min_value=1, max_value=30, value=20, step=1)
taeg_pct     = st.number_input("TAEG — assurance incluse (%)", min_value=0.0, max_value=20.0, value=3.5, step=0.05)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 — REVENUS
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 3. Revenus locatifs")

loyer_hc       = st.number_input("Loyer mensuel HC (€)", min_value=0, value=800, step=50,
                                  help="Hors charges — montant perçu hors provision pour charges")
charges_loca   = st.number_input("Charges locataires récupérables (€/mois)", min_value=0, value=0, step=10,
                                  help="Provision pour charges payée par le locataire en plus du loyer HC. S'ajoute au cash-flow.")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4 — CHARGES ANNUELLES (propriétaire)
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 4. Charges annuelles (propriétaire)")

gestion_pct    = st.number_input("Gestion locative (%)", min_value=0.0, max_value=30.0, value=0.0, step=0.5,
                                  help="Appliqué sur le loyer HC annuel. 0 si gestion en direct.")
taxe_fonciere  = st.number_input("Taxe foncière (€/an)",               min_value=0, value=800, step=50)
assurance_pno  = st.number_input("Assurance PNO (€/an)",               min_value=0, value=150, step=10,
                                  help="150 €/lot habitation — 350 €/lot commerce")
charges_copro  = st.number_input("Charges de copropriété (€/an)",      min_value=0, value=0,   step=100,
                                  help="0 € si maison individuelle")
charges_fluides= st.number_input("Électricité / eau / internet (€/an)",min_value=0, value=0,   step=100,
                                  help="0 € si à la charge du locataire")

# ═════════════════════════════════════════════════════════════════════════════
# CALCULS (tous ici, après tous les inputs)
# ═════════════════════════════════════════════════════════════════════════════

taeg = taeg_pct / 100
loyer_hc_annuel = loyer_hc * 12

# Acquisition
total_sans_garantie = prix + frais_notaire + frais_dossier + travaux + mobilier
emprunt_brut        = max(0, total_sans_garantie - apport)
frais_garantie      = round(emprunt_brut * 0.012)
total_projet        = total_sans_garantie + frais_garantie
emprunt             = max(0, total_projet - apport)
frais_garantie      = round(emprunt * 0.012)          # 2e passe (converge)
total_projet        = total_sans_garantie + frais_garantie
emprunt             = max(0, total_projet - apport)

# Financement
mensualite_val = mensualite(emprunt, taeg, int(duree_ans))

# Charges propriétaire
gestion_val        = round(loyer_hc_annuel * gestion_pct / 100)
total_charges_ann  = gestion_val + taxe_fonciere + assurance_pno + charges_copro + charges_fluides

# Résultats
rendement_brut = (loyer_hc_annuel / total_projet * 100) if total_projet > 0 else 0.0
rendement_net  = ((loyer_hc_annuel - total_charges_ann) / total_projet * 100) if total_projet > 0 else 0.0

# Cash-flow : loyer HC + charges récupérables - mensualité - charges proprio
cashflow = loyer_hc + charges_loca - mensualite_val - (total_charges_ann / 12)

cap10 = capital_rembourse(emprunt, taeg, int(duree_ans), 10)
cap20 = capital_rembourse(emprunt, taeg, int(duree_ans), 20)

# ═════════════════════════════════════════════════════════════════════════════
# AFFICHAGE RÉCAPITULATIF
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("### Récapitulatif")

# Bloc acquisition
st.markdown(f"""
<div class="bloc">
  <div class="bloc-title">Acquisition</div>
  <div class="ligne"><span>Prix négocié FAI</span><span class="val">{fmt(prix)}</span></div>
  <div class="ligne"><span>Frais de notaire ({frais_notaire_pct}%)</span><span class="val">{fmt(frais_notaire)}</span></div>
  <div class="ligne"><span>Frais de dossier bancaires</span><span class="val">{fmt(frais_dossier)}</span></div>
  <div class="ligne"><span>Frais de garantie bancaire (1,2%)</span><span class="val">{fmt(frais_garantie)}</span></div>
  <div class="ligne"><span>Travaux</span><span class="val">{fmt(travaux)}</span></div>
  <div class="ligne"><span>Mobilier</span><span class="val">{fmt(mobilier)}</span></div>
  <div class="ligne total"><span>TOTAL PROJET</span><span class="val">{fmt(total_projet)}</span></div>
</div>
""", unsafe_allow_html=True)

# Bloc financement
st.markdown(f"""
<div class="bloc">
  <div class="bloc-title">Financement</div>
  <div class="ligne"><span>Apport</span><span class="val">{fmt(apport)}</span></div>
  <div class="ligne total"><span>Emprunt</span><span class="val">{fmt(emprunt)}</span></div>
  <div class="ligne"><span>Mensualité</span><span class="val">{fmt(mensualite_val)} / mois</span></div>
</div>
""", unsafe_allow_html=True)

# Bloc revenus & charges
st.markdown(f"""
<div class="bloc">
  <div class="bloc-title">Revenus & Charges mensuels</div>
  <div class="ligne"><span>Loyer HC</span><span class="val">+ {fmt(loyer_hc)} / mois</span></div>
  <div class="ligne"><span>Charges locataire récupérables</span><span class="val">+ {fmt(charges_loca)} / mois</span></div>
  <div class="ligne"><span>Mensualité emprunt</span><span class="val">− {fmt(mensualite_val)} / mois</span></div>
  <div class="ligne"><span>Charges propriétaire ({fmt(total_charges_ann)} / an)</span><span class="val">− {fmt(total_charges_ann/12)} / mois</span></div>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# RÉSULTATS
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("### Résultats")

# Cash-flow principal
cf_class = "vert" if cashflow > 0 else ("rouge" if cashflow < 0 else "bleu")
cf_sign  = "+" if cashflow >= 0 else ""

st.markdown(f"""
<div class="result-box {cf_class}">
  <div class="result-label">Cash-flow mensuel net avant impôt</div>
  <div class="result-value {cf_class}">{cf_sign}{cashflow:,.0f} €</div>
  <div class="result-unit">par mois</div>
</div>
""", unsafe_allow_html=True)

# Grille KPI — 4 indicateurs clés style dashboard
rn_cls  = "vert" if rendement_net >= 0 else "rouge"
val10   = f"{cap10:,.0f} €" if cap10 is not None else "—"
val20   = f"{cap20:,.0f} €" if cap20 is not None else "—"

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">Rendement brut</div>
    <div class="kpi-value">{rendement_brut:.2f} %</div>
    <div class="kpi-sub">Loyer annuel / Total projet</div>
  </div>
  <div class="kpi-card {'green' if rendement_net >= 0 else 'red'}">
    <div class="kpi-label">Rendement net de charges</div>
    <div class="kpi-value">{rendement_net:.2f} %</div>
    <div class="kpi-sub">Après déduction charges proprio</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-label">Capital remboursé à 10 ans</div>
    <div class="kpi-value">{val10}</div>
    <div class="kpi-sub">Enrichissement patrimonial</div>
  </div>
  <div class="kpi-card purple">
    <div class="kpi-label">Capital remboursé à 20 ans</div>
    <div class="kpi-value">{val20}</div>
    <div class="kpi-sub">Enrichissement patrimonial</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Bouton CTA (bas de page uniquement) ──────────────────────────────────────
st.markdown("""
<a class="cta-btn" href="https://calendar.app.google/54cCfHMosWJSd2zRA" target="_blank">
  📅 Prendre rendez-vous — Investissement clé en main
</a>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<footer>
  Simulateur indicatif avant impôt. Ne constitue pas un conseil fiscal ou financier.
</footer>
""", unsafe_allow_html=True)
