import streamlit as st

st.set_page_config(
    page_title="Calculateur Cash-Flow Immo",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700;800&family=Barlow+Condensed:wght@600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
    background-color: #f4f4f2;
}

/* ── Titre H1 ── */
h1 {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    color: #0d0d0d !important;
    letter-spacing: 0.02em !important;
    text-transform: uppercase !important;
}

/* ── Titres de section H3 ── */
h3 {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.18em !important;
    color: #b8975a !important;
    margin-top: 2rem !important;
    margin-bottom: 0.6rem !important;
}

/* ── Ligne séparatrice ── */
hr { border-color: #e0dcd6 !important; margin: 1.5rem 0 !important; }

/* ── Blocs récapitulatifs ── */
.bloc {
    background: #1a1a18;
    border-radius: 10px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 0.75rem;
}

.bloc-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: #b8975a;
    margin-bottom: 0.9rem;
}

.ligne {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #2a2a28;
    font-size: 0.9rem;
    color: #c8c4bc;
    font-weight: 300;
}
.ligne:last-child { border-bottom: none; }
.ligne .val { font-weight: 600; color: #f0ece4; }
.ligne.total {
    font-weight: 700;
    color: #f0ece4;
    font-size: 0.95rem;
    margin-top: 0.2rem;
    padding-top: 0.65rem;
    border-top: 1px solid #b8975a;
    border-bottom: none;
}
.ligne.total .val { color: #b8975a; font-size: 1.05rem; }

/* ── Carte résultat principal ── */
.result-box {
    border-radius: 10px;
    padding: 2.2rem 1.5rem;
    text-align: center;
    margin-bottom: 0.75rem;
}
.result-box.vert {
    background: #1a1a18;
    border: 1px solid #2a2a28;
    border-left: 4px solid #4ade80;
}
.result-box.rouge {
    background: #1a1a18;
    border: 1px solid #2a2a28;
    border-left: 4px solid #f87171;
}
.result-box.bleu {
    background: #1a1a18;
    border: 1px solid #2a2a28;
    border-left: 4px solid #b8975a;
}

.result-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: #7a756c;
    margin-bottom: 0.6rem;
}
.result-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 4rem;
    font-weight: 700;
    line-height: 1;
    color: #f0ece4;
}
.result-value.vert  { color: #4ade80; }
.result-value.rouge { color: #f87171; }
.result-unit {
    font-size: 0.85rem;
    color: #7a756c;
    margin-top: 0.4rem;
    letter-spacing: 0.05em;
}

/* ── Métriques secondaires ── */
.metric-row {
    background: #1a1a18;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.6rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.9rem;
    color: #c8c4bc;
    font-weight: 300;
}
.metric-row .mval {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 1.2rem;
    color: #f0ece4;
}
.metric-row .mval.vert  { color: #4ade80; }
.metric-row .mval.rouge { color: #f87171; }

/* ── Bouton CTA ── */
.cta-btn {
    display: block;
    text-align: center;
    background: #b8975a;
    color: #0d0d0d !important;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    text-decoration: none !important;
    margin-top: 2rem;
    box-shadow: 0 4px 20px rgba(184,151,90,0.25);
}

/* ── Gate email ── */
.email-wrapper { max-width: 460px; margin: 4rem auto; text-align: center; }
.legal { font-size: 0.72rem; color: #9ca3af; margin-top: 0.8rem; }

/* ── Footer ── */
footer {
    font-size: 0.72rem;
    color: #7a756c;
    text-align: center;
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #e0dcd6;
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

# Rendements
rn_cls = "vert" if rendement_net >= 0 else "rouge"
st.markdown(f"""
<div class="metric-row">
  <span>Rendement brut</span>
  <span class="mval">{rendement_brut:.2f} %</span>
</div>
<div class="metric-row">
  <span>Rendement net de charges</span>
  <span class="mval {rn_cls}">{rendement_net:.2f} %</span>
</div>
""", unsafe_allow_html=True)

# Capital remboursé
val10 = f"{cap10:,.0f} €" if cap10 is not None else "—"
val20 = f"{cap20:,.0f} €" if cap20 is not None else "—"
st.markdown(f"""
<div class="metric-row">
  <span>Capital remboursé à 10 ans</span>
  <span class="mval">{val10}</span>
</div>
<div class="metric-row">
  <span>Capital remboursé à 20 ans</span>
  <span class="mval">{val20}</span>
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
