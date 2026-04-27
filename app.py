import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets as _secrets
from datetime import datetime

st.set_page_config(
    page_title="Calculateur Cash-Flow Immo",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

h1 { font-size: 1.7rem !important; font-weight: 700 !important; color: #124660 !important; }

.bloc {
    background: #F4EBD6;
    border: 1px solid #C7DBC2;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}

.bloc-title {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #1B9476;
    margin-bottom: 0.9rem;
}

.ligne {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid #C7DBC2;
    font-size: 0.92rem;
    color: #124660;
}
.ligne:last-child { border-bottom: none; }
.ligne .val { font-weight: 600; color: #124660; }
.ligne.total { font-weight: 700; color: #124660; font-size: 0.97rem; }
.ligne.total .val { color: #1B9476; }

.result-box {
    border-radius: 14px;
    padding: 2rem 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
}
.result-box.vert  { background: linear-gradient(135deg, #1B9476, #8BD59E); color: white; }
.result-box.rouge { background: linear-gradient(135deg, #7f1d1d, #dc2626); color: white; }
.result-box.bleu  { background: linear-gradient(135deg, #124660, #1B9476); color: white; }

.result-label { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.12em; opacity: 0.85; margin-bottom: 0.5rem; }
.result-value { font-size: 3.2rem; font-weight: 700; line-height: 1; }
.result-unit  { font-size: 1rem; opacity: 0.85; margin-top: 0.3rem; }

.metric-row {
    background: #F4EBD6;
    border: 1px solid #C7DBC2;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.92rem;
    color: #124660;
}
.metric-row .mval { font-weight: 700; font-size: 1.05rem; color: #124660; }
.metric-row .mval.vert  { color: #1B9476; }
.metric-row .mval.rouge { color: #dc2626; }

.cta-btn {
    display: block;
    text-align: center;
    background: #1B9476;
    color: white !important;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.9rem 1rem;
    border-radius: 10px;
    text-decoration: none !important;
    margin-top: 2rem;
    box-shadow: 0 4px 14px rgba(27,148,118,0.3);
}

.email-wrapper {
    max-width: 460px;
    margin: 4rem auto;
    text-align: center;
}
.email-wrapper h2 { font-size: 1.5rem; font-weight: 700; color: #124660; margin-bottom: 0.4rem; }
.email-wrapper p  { font-size: 0.9rem; color: #1B9476; margin-bottom: 1.5rem; }
.legal { font-size: 0.72rem; color: #8BD59E; margin-top: 0.8rem; }

footer {
    font-size: 0.72rem; color: #8BD59E;
    text-align: center; margin-top: 3rem;
    padding-top: 1rem; border-top: 1px solid #C7DBC2;
}
</style>
""", unsafe_allow_html=True)

# ── Fonctions calcul ──────────────────────────────────────────────────────────

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
    return f"{n:,.0f} €".replace(",", " ")

# ── Google Sheets ─────────────────────────────────────────────────────────────

def get_gsheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    # Convertir le dict secrets en dict Python standard
    # et corriger les \n littéraux dans la private_key (problème TOML Streamlit)
    sa_info = dict(st.secrets["google_service_account"])
    sa_info["private_key"] = sa_info["private_key"].replace("\\n", "\n")
    creds = Credentials.from_service_account_info(sa_info, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(st.secrets["gsheets"]["sheet_id"])
    return sheet.worksheet("Emails")

def find_row_by_email(ws, email):
    try:
        cell = ws.find(email, in_column=1)
        if cell:
            return cell.row, ws.row_values(cell.row)
        return None, None
    except gspread.exceptions.CellNotFound:
        return None, None

def find_row_by_token(ws, token):
    try:
        cell = ws.find(token, in_column=5)
        if cell:
            return cell.row, ws.row_values(cell.row)
        return None, None
    except gspread.exceptions.CellNotFound:
        return None, None

def register_new_email(ws, email, token):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([email, now, "en_attente", "", token])

def update_token_for_row(ws, row_idx, token):
    ws.update_cell(row_idx, 5, token)

def validate_email_by_token(ws, token):
    row_idx, row_data = find_row_by_token(ws, token)
    if row_idx is None:
        return None
    email = row_data[0] if row_data else ""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.update_cell(row_idx, 3, "validé")
    ws.update_cell(row_idx, 4, now)
    return email

# ── Email ─────────────────────────────────────────────────────────────────────

def send_validation_email(recipient_email: str, token: str, app_url: str):
    activation_link = f"{app_url}?token={token}"
    sender = st.secrets["gmail"]["sender"]
    password = st.secrets["gmail"]["password"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "✅ Votre accès au Calculateur Cash-Flow Immo — par David V."
    msg["From"] = sender
    msg["To"] = recipient_email

    html = f"""
    <html>
    <body style="font-family:Arial,Helvetica,sans-serif;color:#222;max-width:560px;margin:0 auto;">
    <p>Bonjour,</p>
    <p>Merci pour votre inscription au <strong>Calculateur Cash-Flow Immo Avant Impôt</strong>.</p>
    <p>Cliquez sur le bouton ci-dessous pour valider votre email et accéder gratuitement à l'outil :</p>
    <p style="text-align:center;margin:2rem 0;">
      <a href="{activation_link}"
         style="background:#1B9476;color:white;padding:14px 28px;
                border-radius:8px;text-decoration:none;font-weight:bold;font-size:1rem;">
        ACCÉDER AU CALCULATEUR →
      </a>
    </p>
    <p style="font-size:0.85rem;color:#6b7280;">Ce lien est personnel et valable 48h.</p>
    <br>
    <p>À très vite,</p>
    <p>
      <strong>David V.</strong><br>
      Conseiller en investissement immobilier clé en main<br>
      Hauts-de-France
    </p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient_email, msg.as_string())

# ── Session state ─────────────────────────────────────────────────────────────

if "access_granted" not in st.session_state:
    st.session_state.access_granted = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "token_just_validated" not in st.session_state:
    st.session_state.token_just_validated = False
if "validation_sent" not in st.session_state:
    st.session_state.validation_sent = False

# ── Vérification token dans l'URL ─────────────────────────────────────────────

url_token = st.query_params.get("token", None)

if url_token and not st.session_state.access_granted:
    with st.spinner("Validation de votre email en cours…"):
        try:
            ws = get_gsheet()
            validated_email = validate_email_by_token(ws, url_token)
            if validated_email:
                st.session_state.access_granted = True
                st.session_state.user_email = validated_email
                st.session_state.token_just_validated = True
                st.query_params.clear()
                st.rerun()
            else:
                st.error("❌ Lien invalide ou déjà utilisé. Saisissez votre email pour recevoir un nouveau lien.")
        except Exception as e:
            st.error(f"Erreur validation token : {type(e).__name__} — {str(e)[:500]}")

# ── Gate email ────────────────────────────────────────────────────────────────

if not st.session_state.access_granted:
    st.markdown('<div class="email-wrapper">', unsafe_allow_html=True)
    st.markdown("## 🏠 Calculateur Cash-Flow Immo")

    if st.session_state.validation_sent:
        st.success("📧 Un email de validation vous a été envoyé. Cliquez sur le lien pour accéder au calculateur.")
        st.info("Vous n'avez pas reçu l'email ? Vérifiez vos spams ou ressaisissez votre adresse ci-dessous.")
    else:
        st.markdown("Entrez votre email pour accéder gratuitement à l'outil :")

    with st.form("gate"):
        email_input = st.text_input("Email", placeholder="vous@exemple.com", label_visibility="collapsed")
        ok = st.form_submit_button("Accéder au calculateur →", use_container_width=True, type="primary")

        if ok:
            email_clean = email_input.strip().lower()
            if not ("@" in email_clean and "." in email_clean.split("@")[-1]):
                st.error("Adresse email invalide.")
            else:
                app_url = st.secrets.get("app", {}).get("url", "https://votre-app.streamlit.app")
                try:
                    ws = get_gsheet()
                    row_idx, row_data = find_row_by_email(ws, email_clean)

                    if row_data:
                        statut = row_data[2] if len(row_data) > 2 else ""
                        if statut == "validé":
                            # CAS B — accès direct
                            st.session_state.user_email = email_clean
                            st.session_state.access_granted = True
                            st.rerun()
                        else:
                            # CAS C — en_attente → renvoi token
                            new_token = _secrets.token_urlsafe(32)
                            update_token_for_row(ws, row_idx, new_token)
                            send_validation_email(email_clean, new_token, app_url)
                            st.session_state.validation_sent = True
                            st.rerun()
                    else:
                        # CAS A — nouvel email
                        new_token = _secrets.token_urlsafe(32)
                        register_new_email(ws, email_clean, new_token)
                        send_validation_email(email_clean, new_token, app_url)
                        st.session_state.validation_sent = True
                        st.rerun()

                except smtplib.SMTPException as e:
                    st.error(f"Erreur lors de l'envoi de l'email : {type(e).__name__} — {str(e)[:300]}")
                except Exception as e:
                    st.error(f"Erreur BDD : {type(e).__name__} — {str(e)[:500]}")

    st.markdown('<p class="legal">En renseignant votre email, vous acceptez d\'être recontacté par David V.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ── Bandeau confirmation validation ───────────────────────────────────────────

if st.session_state.token_just_validated:
    st.success("✅ Email validé ! Bienvenue dans le calculateur.")
    st.session_state.token_just_validated = False

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

loyer_hc     = st.number_input("Loyer mensuel HC (€)", min_value=0, value=800, step=50,
                                help="Hors charges — montant perçu hors provision pour charges")
charges_loca = st.number_input("Charges locataires récupérables (€/mois)", min_value=0, value=0, step=10,
                                help="Provision pour charges payée par le locataire en plus du loyer HC. S'ajoute au cash-flow.")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4 — CHARGES ANNUELLES (propriétaire)
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 4. Charges annuelles (propriétaire)")

gestion_pct     = st.number_input("Gestion locative (%)", min_value=0.0, max_value=30.0, value=0.0, step=0.5,
                                   help="Appliqué sur le loyer HC annuel. 0 si gestion en direct.")
taxe_fonciere   = st.number_input("Taxe foncière (€/an)",                min_value=0, value=800, step=50)
assurance_pno   = st.number_input("Assurance PNO (€/an)",                min_value=0, value=150, step=10,
                                   help="150 €/lot habitation — 350 €/lot commerce")
charges_copro   = st.number_input("Charges de copropriété (€/an)",       min_value=0, value=0,   step=100,
                                   help="0 € si maison individuelle")
charges_fluides = st.number_input("Électricité / eau / internet (€/an)", min_value=0, value=0,   step=100,
                                   help="0 € si à la charge du locataire")

# ═════════════════════════════════════════════════════════════════════════════
# CALCULS
# ═════════════════════════════════════════════════════════════════════════════

taeg = taeg_pct / 100
loyer_hc_annuel = loyer_hc * 12

total_sans_garantie = prix + frais_notaire + frais_dossier + travaux + mobilier
emprunt_brut        = max(0, total_sans_garantie - apport)
frais_garantie      = round(emprunt_brut * 0.012)
total_projet        = total_sans_garantie + frais_garantie
emprunt             = max(0, total_projet - apport)
frais_garantie      = round(emprunt * 0.012)
total_projet        = total_sans_garantie + frais_garantie
emprunt             = max(0, total_projet - apport)

mensualite_val     = mensualite(emprunt, taeg, int(duree_ans))
gestion_val        = round(loyer_hc_annuel * gestion_pct / 100)
total_charges_ann  = gestion_val + taxe_fonciere + assurance_pno + charges_copro + charges_fluides

rendement_brut = (loyer_hc_annuel / total_projet * 100) if total_projet > 0 else 0.0
rendement_net  = ((loyer_hc_annuel - total_charges_ann) / total_projet * 100) if total_projet > 0 else 0.0
cashflow       = loyer_hc + charges_loca - mensualite_val - (total_charges_ann / 12)

cap10 = capital_rembourse(emprunt, taeg, int(duree_ans), 10)
cap20 = capital_rembourse(emprunt, taeg, int(duree_ans), 20)

# ═════════════════════════════════════════════════════════════════════════════
# AFFICHAGE RÉCAPITULATIF
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("### Récapitulatif")

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

st.markdown(f"""
<div class="bloc">
  <div class="bloc-title">Financement</div>
  <div class="ligne"><span>Apport</span><span class="val">{fmt(apport)}</span></div>
  <div class="ligne total"><span>Emprunt</span><span class="val">{fmt(emprunt)}</span></div>
  <div class="ligne"><span>Mensualité</span><span class="val">{fmt(mensualite_val)} / mois</span></div>
</div>
""", unsafe_allow_html=True)

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

cf_class = "vert" if cashflow > 0 else ("rouge" if cashflow < 0 else "bleu")
cf_sign  = "+" if cashflow >= 0 else ""

st.markdown(f"""
<div class="result-box {cf_class}">
  <div class="result-label">Cash-flow mensuel net avant impôt</div>
  <div class="result-value">{cf_sign}{cashflow:,.0f} €</div>
  <div class="result-unit">par mois</div>
</div>
""", unsafe_allow_html=True)

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

st.markdown("""
<a class="cta-btn" href="https://calendar.app.google/54cCfHMosWJSd2zRA" target="_blank">
  📅 Prendre rendez-vous — Investissement clé en main
</a>
""", unsafe_allow_html=True)

st.markdown("""
<footer>
  Simulateur indicatif avant impôt. Ne constitue pas un conseil fiscal ou financier.
</footer>
""", unsafe_allow_html=True)
