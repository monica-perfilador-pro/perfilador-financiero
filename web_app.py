import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="AutoScore AI", page_icon="🚗", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Exo+2:wght@300;400;500;600;700&display=swap');

/* =============================================
   BASE
============================================= */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], section.main {
    background: #050c1a !important;
    color: #e2e8f0 !important;
}

/* GRID OVERLAY */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(56,189,248,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,189,248,0.035) 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none; z-index: 0;
}

/* GLOW TOP */
[data-testid="stMain"]::before {
    content: "";
    position: fixed; top: -200px; left: 50%;
    transform: translateX(-50%);
    width: 1200px; height: 500px;
    background: radial-gradient(ellipse,
        rgba(56,189,248,0.09) 0%, rgba(99,102,241,0.06) 40%, transparent 70%);
    filter: blur(60px);
    pointer-events: none; z-index: 0;
}

.block-container {
    position: relative; z-index: 1;
    padding: 1rem 2rem 2rem 2rem !important;
    max-width: 100% !important;
}

*, *::before, *::after {
    font-family: 'Exo 2', sans-serif !important;
    box-sizing: border-box;
}

/* =============================================
   HEADER SUPERIOR (logo + titulo)
============================================= */
.top-header {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 0 0 20px 0;
    border-bottom: 1px solid rgba(56,189,248,0.12);
    margin-bottom: 24px;
}
.top-header img { height: 54px; }
.top-header-text h1 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.7rem !important;
    font-weight: 700 !important;
    color: #e2e8f0 !important;
    letter-spacing: 0.08em !important;
    margin: 0 !important; line-height: 1 !important;
}
.top-header-text p {
    color: #38bdf8;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 4px 0 0 0;
}

/* DIVISOR VERTICAL */
.divider-v {
    width: 1px;
    background: linear-gradient(180deg,
        transparent 0%, rgba(56,189,248,0.35) 20%,
        rgba(56,189,248,0.35) 80%, transparent 100%);
    min-height: 100vh;
    position: absolute;
    left: 50%;
    top: 0;
}

/* =============================================
   PANEL IZQUIERDO — formulario
============================================= */
.panel-left {
    padding-right: 20px;
    border-right: 1px solid rgba(56,189,248,0.1);
}

/* =============================================
   PANEL DERECHO — resultados
============================================= */
.panel-right {
    padding-left: 20px;
}

/* PLACEHOLDER cuando no hay resultado */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    gap: 16px;
    opacity: 0.4;
}
.empty-state .icon { font-size: 3.5rem; }
.empty-state p {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-align: center;
}

/* =============================================
   CARDS
============================================= */
.card-section {
    background: linear-gradient(160deg, rgba(8,18,38,0.97) 0%, rgba(5,12,28,0.99) 100%);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 16px;
    padding: 20px 22px 22px;
    margin-bottom: 18px;
    position: relative; overflow: hidden;
    box-shadow:
        0 0 0 1px rgba(56,189,248,0.03),
        0 16px 50px rgba(0,0,0,0.55),
        inset 0 1px 0 rgba(255,255,255,0.04);
}
.card-section::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg,
        transparent, rgba(56,189,248,0.65) 30%,
        rgba(139,92,246,0.45) 70%, transparent);
}
.card-section::after {
    content: "";
    position: absolute; top: -20px; right: -20px;
    width: 130px; height: 130px;
    background: radial-gradient(circle, rgba(56,189,248,0.06), transparent 65%);
    pointer-events: none;
}

.card-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 18px; padding-bottom: 13px;
    border-bottom: 1px solid rgba(56,189,248,0.1);
}
.card-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, rgba(56,189,248,0.16), rgba(139,92,246,0.12));
    border: 1px solid rgba(56,189,248,0.3);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px; flex-shrink: 0;
    box-shadow: 0 0 14px rgba(56,189,248,0.1);
}
.card-title {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem !important; font-weight: 700 !important;
    color: #e2e8f0 !important; letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    margin: 0 !important; line-height: 1 !important;
}

/* =============================================
   INPUTS
============================================= */
.stTextInput input, .stNumberInput input {
    background: rgba(3,9,22,0.92) !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(56,189,248,0.16) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    font-size: 0.88rem !important;
    width: 100% !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: rgba(56,189,248,0.6) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.08), 0 0 16px rgba(56,189,248,0.1) !important;
}
.stTextInput input::placeholder, .stNumberInput input::placeholder {
    color: #1e3a4a !important;
}
.stSelectbox > div > div {
    background: rgba(3,9,22,0.92) !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(56,189,248,0.16) !important;
    border-radius: 10px !important;
    padding: 3px 8px !important;
}
label,
[data-testid="stWidgetLabel"] p {
    color: #38bdf8 !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}
.stNumberInput button {
    background: rgba(56,189,248,0.07) !important;
    border: 1px solid rgba(56,189,248,0.15) !important;
    color: #38bdf8 !important;
    border-radius: 7px !important;
    padding: 3px 10px !important;
    width: auto !important; margin: 0 !important;
}

/* =============================================
   BOTÓN
============================================= */
.stFormSubmitButton > button, .stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 55%, #8b5cf6 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: 50px !important; padding: 14px 28px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important; font-weight: 700 !important;
    letter-spacing: 0.13em !important; text-transform: uppercase !important;
    box-shadow: 0 0 30px rgba(99,102,241,0.4), 0 0 60px rgba(56,189,248,0.1),
        inset 0 1px 0 rgba(255,255,255,0.18) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    margin-top: 8px !important;
}
.stFormSubmitButton > button:hover, .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 45px rgba(99,102,241,0.55), 0 0 80px rgba(56,189,248,0.18) !important;
}

/* =============================================
   EXPANDER OSCURO
============================================= */
details, summary,
[data-testid="stExpander"],
[data-testid="stExpander"] > div,
.streamlit-expanderHeader,
.streamlit-expanderContent {
    background: rgba(3,9,22,0.88) !important;
    border: 1px solid rgba(56,189,248,0.14) !important;
    border-radius: 12px !important;
    color: #7dd3fc !important;
}
.streamlit-expanderHeader p, .streamlit-expanderHeader span,
[data-testid="stExpander"] summary p {
    color: #7dd3fc !important; font-weight: 600 !important;
}
[data-testid="stExpander"] > div > div {
    background: rgba(3,9,22,0.92) !important;
    border-top: 1px solid rgba(56,189,248,0.08) !important;
    border-radius: 0 0 12px 12px !important;
    padding: 14px !important;
}

/* =============================================
   ALERTS
============================================= */
.stSuccess > div {
    background: rgba(34,197,94,0.09) !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
    border-radius: 12px !important; color: #86efac !important;
}
.stWarning > div {
    background: rgba(245,158,11,0.07) !important;
    border: 1px solid rgba(245,158,11,0.28) !important;
    border-radius: 12px !important; color: #fcd34d !important;
}
.stError > div {
    background: rgba(239,68,68,0.07) !important;
    border: 1px solid rgba(239,68,68,0.28) !important;
    border-radius: 12px !important; color: #fca5a5 !important;
}
.stInfo > div {
    background: rgba(56,189,248,0.06) !important;
    border: 1px solid rgba(56,189,248,0.22) !important;
    border-radius: 12px !important; color: #7dd3fc !important;
}

hr { border: none !important; border-top: 1px solid rgba(56,189,248,0.1) !important; margin: 18px 0 !important; }
.stCaption p { color: #f59e0b !important; font-size: 0.75rem !important; }

.stLinkButton a {
    background: linear-gradient(135deg, rgba(56,189,248,0.1), rgba(99,102,241,0.08)) !important;
    border: 1px solid rgba(56,189,248,0.28) !important;
    color: #7dd3fc !important; border-radius: 10px !important;
    font-weight: 600 !important; width: 100% !important;
    display: block !important; text-align: center !important; padding: 11px !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(56,189,248,0.1), rgba(99,102,241,0.08)) !important;
    border: 1px solid rgba(56,189,248,0.28) !important;
    color: #7dd3fc !important; border-radius: 10px !important;
    font-weight: 600 !important; width: 100% !important; padding: 11px !important;
}

/* =============================================
   RESULTADO CARDS (panel derecho)
============================================= */
.result-card {
    background: linear-gradient(160deg, rgba(8,18,38,0.97), rgba(5,12,28,0.99));
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 16px; padding: 20px 22px;
    margin: 10px 0; position: relative; overflow: hidden;
}
.result-card::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #38bdf8, #6366f1, #8b5cf6);
}

.score-display {
    display: flex; align-items: center; gap: 14px; margin-bottom: 12px;
}
.score-emoji { font-size: 2.2rem; line-height: 1; }
.score-name {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.5rem; font-weight: 700; letter-spacing: 0.08em; line-height: 1;
}
.score-desc { color: #64748b; font-size: 0.78rem; margin-top: 3px; }

.prob-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 50px; padding: 6px 16px;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem; font-weight: 700; color: #7dd3fc;
    letter-spacing: 0.05em; margin: 10px 0;
}

.metrics-row { display: flex; gap: 12px; margin-top: 14px; flex-wrap: wrap; }
.metric-box {
    flex: 1; min-width: 110px; border-radius: 12px; padding: 11px 16px;
}
.metric-box.blue { background: rgba(56,189,248,0.07); border: 1px solid rgba(56,189,248,0.17); }
.metric-box.purple { background: rgba(99,102,241,0.07); border: 1px solid rgba(99,102,241,0.17); }
.metric-label { font-size: 0.64rem; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 5px; font-weight: 600; }
.metric-label.blue { color: #7dd3fc; }
.metric-label.purple { color: #a5b4fc; }
.metric-value { font-family: 'Rajdhani', sans-serif !important; font-size: 1.4rem; font-weight: 700; color: #e2e8f0; line-height: 1; }

.msg-cliente {
    background: linear-gradient(135deg, rgba(56,189,248,0.05), rgba(99,102,241,0.03));
    border: 1px solid rgba(56,189,248,0.13);
    border-left: 3px solid #38bdf8;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px; color: #cbd5e1; font-size: 0.86rem;
    line-height: 1.65; margin: 12px 0;
}

.section-label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.75rem; font-weight: 700; color: #38bdf8;
    text-transform: uppercase; letter-spacing: 0.12em;
    margin: 18px 0 8px; display: flex; align-items: center; gap: 8px;
}

.doc-chip {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 6px 12px;
    background: rgba(56,189,248,0.05); border: 1px solid rgba(56,189,248,0.12);
    border-radius: 7px; margin: 3px 3px 3px 0;
    color: #94a3b8; font-size: 0.8rem;
}

.cotitular-banner {
    padding: 12px 16px; margin: 16px 0 12px;
    background: rgba(245,158,11,0.07); border: 1px solid rgba(245,158,11,0.2);
    border-radius: 12px; font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.9rem; font-weight: 700; color: #fcd34d;
    letter-spacing: 0.06em; text-transform: uppercase;
}

.account-box {
    background: linear-gradient(135deg, rgba(8,18,38,0.97), rgba(5,12,28,0.99));
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 12px; padding: 16px 20px; margin-top: 12px;
}

.security-line {
    text-align: center; color: #1e3a4a; font-size: 0.7rem;
    letter-spacing: 0.06em; margin-top: 12px;
    display: flex; align-items: center; justify-content: center; gap: 6px;
}

/* sticky panel derecho */
.sticky-panel {
    position: sticky;
    top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ──────────────────────────────────────────────────
for k, v in {
    "resultado": None, "cotitular_activo": False,
    "cotitular_resultado": None, "analizado": False,
    "ingreso": 0.0, "mensualidad": 0.0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HEADER GLOBAL ──────────────────────────────────────────────────
hcol1, hcol2 = st.columns([1, 5])
with hcol1:
    st.image("logo_new.png", width=120)
with hcol2:
    st.markdown("""
    <div style="padding: 8px 0 0 4px;">
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.8rem;font-weight:700;
            color:#e2e8f0;letter-spacing:0.08em;line-height:1;">AutoScore AI</div>
        <div style="color:#38bdf8;font-size:0.72rem;letter-spacing:0.14em;
            text-transform:uppercase;margin-top:4px;">Aprobación Inteligente</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="height:1px;margin:4px 0 22px;
background:linear-gradient(90deg,transparent,#38bdf8 30%,#8b5cf6 70%,transparent);
box-shadow:0 0 18px rgba(56,189,248,0.35);"></div>
""", unsafe_allow_html=True)

# ─── LAYOUT DOS COLUMNAS ────────────────────────────────────────────
col_form, col_result = st.columns([1, 1], gap="large")

# ╔══════════════════════════════════════════╗
# ║         COLUMNA IZQUIERDA — FORM         ║
# ╚══════════════════════════════════════════╝
with col_form:

    # ASESOR (fuera del form para persistir)
    st.markdown("""
    <div class="card-section">
      <div class="card-header">
        <div class="card-icon">👤</div>
        <p class="card-title">Datos del Asesor</p>
      </div>
    </div>""", unsafe_allow_html=True)
    asesor          = st.text_input("Nombre asesor",   placeholder="Escribe el nombre completo")
    telefono_asesor = st.text_input("Teléfono asesor", placeholder="Ej. 55 1234 5678")
    correo_asesor   = st.text_input("Correo asesor",   placeholder="ejemplo@correo.com")
    rfc             = st.text_input("RFC asesor",      placeholder="Ej. XAXX010101000")
    st.markdown('<div class="security-line">🛡️ Tus datos están protegidos y seguros</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("formulario"):

        # CLIENTE
        st.markdown("""
        <div class="card-section">
          <div class="card-header">
            <div class="card-icon">👥</div>
            <p class="card-title">Datos del Cliente</p>
          </div>
        </div>""", unsafe_allow_html=True)
        nombre_cliente = st.text_input("Nombre cliente",   placeholder="Nombre completo")
        telefono       = st.text_input("Teléfono cliente", placeholder="Ej. 55 9876 5432")
        correo         = st.text_input("Correo cliente",   placeholder="cliente@correo.com")
        st.markdown("<br>", unsafe_allow_html=True)

        # PERFIL
        st.markdown("""
        <div class="card-section">
          <div class="card-header">
            <div class="card-icon">📊</div>
            <p class="card-title">Perfil Financiero</p>
          </div>
        </div>""", unsafe_allow_html=True)
        edad         = st.number_input("Edad", 18, 73, 18)
        ingreso      = st.number_input("Ingreso mensual ($)", min_value=6500.0, value=6500.0, step=500.0, format="%.2f")
        tipo_ingreso = st.selectbox("Tipo de ingreso", ["Nómina","Independiente","No comprueba ingresos"])
        negocio_casa = st.selectbox("¿Negocio en domicilio?", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        if tipo_ingreso == "Independiente":
            st.caption("⚠️ Solo aplica para independientes")
        domicilio    = st.selectbox("Antigüedad domicilio", [1,2,3],
                        format_func=lambda x:["< 1 año","1-3 años","+3 años"][x-1])
        domicilio_buro = st.selectbox("¿Domicilio coincide con identificaciones?", [1,2],
                        format_func=lambda x:"Sí" if x==1 else "No")
        st.markdown("<br>", unsafe_allow_html=True)

        # VEHÍCULO
        st.markdown("""
        <div class="card-section">
          <div class="card-header">
            <div class="card-icon">🚗</div>
            <p class="card-title">Datos del Vehículo</p>
          </div>
        </div>""", unsafe_allow_html=True)
        precio    = st.number_input("Precio del vehículo ($)", min_value=0.0, format="%0.2f")
        enganche  = st.number_input("Enganche ($)", min_value=0.0, format="%0.2f")
        plazo     = st.selectbox("Plazo (meses)", [12,24,36,48,60,72])
        consultas = st.number_input("Consultas / créditos recientes (últimos 3 meses)", 0, 20)
        st.markdown("<br>", unsafe_allow_html=True)

        # HISTORIAL
        st.markdown("""
        <div class="card-section">
          <div class="card-header">
            <div class="card-icon">🏦</div>
            <p class="card-title">Historial Crediticio</p>
          </div>
        </div>""", unsafe_allow_html=True)
        auto         = st.selectbox("Crédito automotriz previo", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        credinissan  = st.selectbox("CrediNissan", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        hipotecario  = st.selectbox("Hipotecario", [1,2,3],
                        format_func=lambda x:["Bancario","Infonavit","No tiene"][x-1])
        tarjeta_alta = st.selectbox("Tarjetas mayores a $100K", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        tarjeta_baja = st.selectbox("Tarjetas menores a $100K o departamentales", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        atrasos      = st.selectbox("Atrasos en buró", [1,2,3],
                        format_func=lambda x:["1-30 días","31-60 días","Más de 61 días"][x-1])
        st.markdown("<br>", unsafe_allow_html=True)

        # PERFIL COMPRA
        st.markdown("""
        <div class="card-section">
          <div class="card-header">
            <div class="card-icon">🔥</div>
            <p class="card-title">Perfil de Compra</p>
          </div>
        </div>""", unsafe_allow_html=True)
        enganche_disp = st.selectbox("¿Tiene enganche disponible?", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        compra_mes    = st.selectbox("¿Compra este mes?", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        unidad        = st.selectbox("¿Hay unidad disponible?", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        st.markdown("<br>", unsafe_allow_html=True)

        submitted = st.form_submit_button("✦  ANALIZAR PERFIL FINANCIERO")

# ─── LÓGICA ─────────────────────────────────────────────────────────
if submitted:
    st.session_state.analizado = True
    st.session_state.ingreso   = ingreso

    monto        = max(precio - enganche, 0)
    tasa_m       = 0.015
    mensualidad  = (monto*(tasa_m*(1+tasa_m)**plazo)/((1+tasa_m)**plazo-1)) if plazo>0 and monto>0 else 0
    st.session_state.mensualidad = mensualidad
    enganche_pct = (enganche/precio)*100 if precio>0 else 0

    riesgo_alto = riesgo_medio = False
    if atrasos==3:                              riesgo_alto=True
    if consultas>=8:                            riesgo_alto=True
    elif consultas>=5:                          riesgo_medio=True
    if tipo_ingreso=="Independiente":           riesgo_medio=True
    if tipo_ingreso=="No comprueba ingresos":   riesgo_alto=True
    if enganche_pct<10:                         riesgo_alto=True
    elif enganche_pct<20:                       riesgo_medio=True

    score=0
    if tarjeta_alta==1:                         score+=4
    if tarjeta_baja==1 and ingreso>30000:       score+=1
    if credinissan==1:                          score+=5
    if auto==1:                                 score+=3
    if hipotecario==1:                          score+=3
    elif hipotecario==2:                        score+=1
    if atrasos==2:                              score-=3
    elif atrasos==3:                            score-=10
    if consultas>=8:                            score-=12
    elif consultas>=5:                          score-=6
    elif consultas>=3:                          score-=3

    perfil = "DELGADO" if score<=0 else ("FUERTE" if score>=7 else "MEDIO")
    prob   = 85 if perfil=="FUERTE" else (65 if perfil=="MEDIO" else 30)
    if enganche_pct>=40:    prob+=10
    elif enganche_pct>=25:  prob+=5
    if consultas>=8:        prob-=25
    elif consultas>=5:      prob-=15
    elif consultas>=3:      prob-=5
    prob = max(5, min(95, prob))

    cap_pago = ingreso/2 if tipo_ingreso=="Nómina" else ingreso/3.33
    excede   = mensualidad > cap_pago

    if compra_mes==2:                                       temp="❄️ FRÍO"
    elif compra_mes==1 and enganche_disp==1 and unidad==1:  temp="🔥 CALIENTE"
    else:                                                   temp="🟡 TIBIO"

    if prob>=80:   sc="AZUL"
    elif prob>=70: sc="VERDE"
    elif prob>=45: sc="AMARILLO"
    elif prob>=35: sc="NARANJA"
    else:          sc="ROJO"

    msg_c=msg_a=""; decision="🟡 EN EVALUACIÓN"; plan="REVISION"

    if consultas>=10:
        decision="🟠 ESTRATEGIA ALTERNATIVA"; plan="COTITULAR"
    elif riesgo_alto and perfil!="FUERTE":
        decision="🟠 ESTRATEGIA ALTERNATIVA"; plan="ALTERNATIVA"
        msg_c="Tu perfil puede avanzar mediante una alternativa de financiamiento."
        msg_a="Riesgo alto: subir enganche ≥10% / comprobar ingresos / buscar cotitular."
    elif atrasos==3:
        decision="🟠 ESTRATEGIA ALTERNATIVA"; plan="ALTERNATIVA"
        msg_c="Tu perfil puede avanzar mediante una alternativa de financiamiento."
        msg_a="Subir enganche / cotitular / evitar consultas."
    elif sc=="ROJO":
        decision="🟠 ESTRATEGIA ALTERNATIVA"; plan="COTITULAR"
        msg_c="Tu perfil actualmente requiere una alternativa de financiamiento."
        msg_a="Cotitular fuerte / Subir enganche / Evitar consultas en buró."
    elif excede and prob<70:
        decision="🟡 AJUSTE NECESARIO"; plan="AJUSTAR_PLAZO"
        msg_c="La mensualidad puede ajustarse para mejorar tu perfil."
        msg_a="Ampliar plazo / Reducir monto / Validar ingresos."
    elif riesgo_medio and prob<60:
        decision="🟠 PERFIL CON OPORTUNIDAD"; plan="RESCATE"
        msg_c="Tu perfil tiene alta posibilidad de avanzar ajustando puntos clave."
        msg_a="Enganche ≥25% / Cotitular línea directa / Evitar más consultas."
    elif prob>=70:
        if riesgo_medio:
            decision="🟢 APROBADO EN ANÁLISIS DE FINANCIERA"; plan="SE VA A ANALISIS"
            msg_c="Tu perfil es viable y puede avanzar a proceso de aprobación."
            msg_a="Validación de ingresos / Investigación telefónica."
        else:
            decision="🟢 APROBADO"; plan="AUTOMATICO"
            msg_c="Tu perfil cumple los criterios para avanzar en automático."
            msg_a="Perfil limpio. Proceder directo."
    elif prob>=50:
        if enganche_pct<20 or riesgo_medio:
            decision="🟡 APROBABLE CON AJUSTES"; plan="CONDICIONADO"
            msg_c="Tu perfil es viable realizando algunos ajustes."
            msg_a="Subir enganche +15pts / Validación por financiera."
        else:
            decision="🟡 PRE APROBADO"; plan="DIRECTO"
            msg_c="Tu perfil es favorable para avanzar."
            msg_a="Perfil estable. Proceder."
    elif prob>=35:
        decision="🟡 PERFIL MEJORABLE"; plan="COTITULAR"
        msg_c="Tu perfil puede fortalecerse con apoyo adicional."
        msg_a="Cotitular fuerte / Comprobar ingresos / Mejorar enganche."
    else:
        decision="🟠 ESTRATEGIA ALTERNATIVA"; plan="ALTERNATIVA"
        msg_c="Tu perfil puede avanzar mediante una alternativa de financiamiento."
        msg_a="Financiera flexible / Reestructura de perfil."

    inv="🟢 Sin validaciones relevantes"
    if tipo_ingreso!="Nómina" and prob<45:     inv="🔴 Validación adicional requerida"
    if domicilio_buro==2:                      inv="🔴 Validación de domicilio"
    if tipo_ingreso=="Independiente":          inv="🟡 Validación de ingresos"
    if tipo_ingreso=="Independiente" and negocio_casa==1:
        prob=max(prob,80); inv="🔴 Requiere validación física"

    docs=["INE","Comprobante de domicilio"]
    if plan=="DIRECTO":          docs=["INE","Comprobante","Cotización"]
    elif plan=="COTITULAR":      docs+=["Cotitular obligatorio"]
    elif tipo_ingreso=="Nómina": docs+=["Nómina","Estado de cuenta"]
    else:                        docs+=["Estados de cuenta"]

    st.session_state.resultado = {
        "score_color":sc, "prob":prob, "temp":temp,
        "investigacion":inv, "decision":decision, "plan":plan,
        "mensaje_cliente":msg_c, "mensaje_asesor":msg_a,
        "nombre":nombre_cliente, "telefono":telefono, "correo":correo,
        "asesor":asesor, "telefono_asesor":telefono_asesor,
        "correo_asesor":correo_asesor, "rfc":rfc,
        "documentos":docs, "mensualidad":mensualidad, "capacidad_pago":cap_pago,
    }
    st.session_state.cotitular_activo    = (plan=="COTITULAR")
    st.session_state.cotitular_resultado = None

# ╔══════════════════════════════════════════╗
# ║       COLUMNA DERECHA — RESULTADOS       ║
# ╚══════════════════════════════════════════╝
with col_result:

    if not st.session_state.resultado:
        st.markdown("""
        <div class="empty-state">
          <div class="icon">📊</div>
          <p>Aquí aparecerá el análisis<br>del perfil del cliente</p>
          <div style="width:60px;height:1px;background:rgba(56,189,248,0.3);margin:4px auto;"></div>
          <p style="font-size:0.7rem;opacity:0.6;">Completa el formulario y presiona<br>ANALIZAR PERFIL</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        r = st.session_state.resultado

        SCORE_MAP = {
            "AZUL":     ("🔵","SCORE AZUL",    "#38bdf8","Perfil fuerte — alta probabilidad"),
            "VERDE":    ("🟢","SCORE VERDE",   "#22c55e","Buen perfil — condiciones normales"),
            "AMARILLO": ("🟡","SCORE AMARILLO","#eab308","Perfil medio — validación adicional"),
            "NARANJA":  ("🟠","SCORE NARANJA", "#f97316","Perfil débil — cotitular / enganche"),
            "ROJO":     ("🔴","EN DESARROLLO", "#ef4444","Estrategia alternativa requerida"),
        }
        em, lbl, col_hex, dsc = SCORE_MAP[r["score_color"]]

        # SCORE CARD
        st.markdown(f"""
        <div class="result-card">
          <div class="score-display">
            <span class="score-emoji">{em}</span>
            <div>
              <div class="score-name" style="color:{col_hex};">{lbl}</div>
              <div class="score-desc">{dsc}</div>
            </div>
          </div>
          <div class="prob-badge">⚡ Probabilidad: {r['prob']}%</div>
          <div class="metrics-row">
            <div class="metric-box blue">
              <div class="metric-label blue">Capacidad de pago</div>
              <div class="metric-value">${r['capacidad_pago']:,.0f}</div>
            </div>
            <div class="metric-box purple">
              <div class="metric-label purple">Mensualidad estimada</div>
              <div class="metric-value">${r['mensualidad']:,.0f}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # DECISIÓN
        if "APROBADO" in r["decision"]:
            st.success(r["decision"])
        elif "ALTERNATIVA" in r["decision"] or "OPORTUNIDAD" in r["decision"] or "AJUSTE" in r["decision"]:
            st.warning(r["decision"])
        else:
            st.info(r["decision"])

        if r.get("mensaje_cliente"):
            st.markdown(f'<div class="msg-cliente">💡 {r["mensaje_cliente"]}</div>', unsafe_allow_html=True)

        # ESTRATEGIA INTERNA
        with st.expander("🔒 Estrategia interna — solo asesor"):
            st.markdown(f"""
            <div style="background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.18);
                border-left:3px solid #ef4444;border-radius:0 10px 10px 0;
                padding:12px 16px;color:#fca5a5;font-size:0.86rem;line-height:1.6;">
                🔴 {r.get("mensaje_asesor","")}
            </div>
            """, unsafe_allow_html=True)

        # TEMPERATURA
        st.markdown('<div class="section-label">🔥 Temperatura de venta</div>', unsafe_allow_html=True)
        if "CALIENTE" in r["temp"]:  st.success(r["temp"])
        elif "TIBIO" in r["temp"]:   st.warning(r["temp"])
        else:                        st.info(r["temp"])

        # VALIDACIONES
        st.markdown('<div class="section-label">🔎 Validaciones requeridas</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:rgba(56,189,248,0.04);border:1px solid rgba(56,189,248,0.1);
            border-radius:10px;padding:11px 15px;color:#cbd5e1;font-size:0.86rem;">
            {r["investigacion"]}
        </div>""", unsafe_allow_html=True)

        # DOCUMENTOS
        st.markdown('<div class="section-label">📄 Documentación</div>', unsafe_allow_html=True)
        docs_html = "".join([f'<span class="doc-chip">📎 {d}</span>' for d in r["documentos"]])
        st.markdown(f'<div>{docs_html}</div>', unsafe_allow_html=True)

        # SIGUIENTE PASO
        st.markdown('<div class="section-label">💰 Siguiente paso</div>', unsafe_allow_html=True)
        if r["plan"]=="DIRECTO": st.success("👉 Solicitar ENGANCHE COMPLETO")
        else:                    st.warning("👉 Solicitar APARTADO $5,000")
        st.error("⚠️ Solicita anticipo para asegurar unidad")

        st.markdown("""
        <div class="account-box">
          <div style="font-family:'Rajdhani',sans-serif;font-size:0.68rem;font-weight:700;
              color:#38bdf8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:7px;">
              🏦 Cuenta BBVA</div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:600;
              color:#e2e8f0;">DAOSA SA DE CV</div>
          <div style="color:#475569;font-size:0.84rem;margin-top:3px;letter-spacing:0.04em;">
              012320001250476847</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("📊 Abrir Cotizador",
            "https://procotiza.losnrtelepro.com.mx/Procotiza/login.aspx?mns",
            use_container_width=True)

        # COTITULAR
        if st.session_state.cotitular_activo:
            st.markdown('<div class="cotitular-banner">👥 Análisis de Cotitular Requerido</div>',
                unsafe_allow_html=True)
            with st.form("formulario_cotitular"):
                tipo_cot         = st.selectbox("Tipo cotitular", ["Línea directa","Conocido"])
                ingreso_cot      = st.number_input("Ingreso cotitular ($)", min_value=0.0, step=500.0)
                auto_cot         = st.selectbox("Automotriz cotitular", ["Sí","No"])
                credinissan_cot  = st.selectbox("CrediNissan cotitular", ["Sí","No"])
                hipotecario_cot  = st.selectbox("Hipotecario cotitular", ["No tiene","Infonavit","Bancario"])
                tarjeta_alta_cot = st.selectbox("Tarjetas >$100K cotitular", ["Sí","No"])
                atrasos_cot      = st.selectbox("Buró cotitular", ["Sin atrasos","1-30 días","31-60 días","61+ días"])
                submit_cot       = st.form_submit_button("✦  EVALUAR COTITULAR")

            if submit_cot:
                sc2=0
                if auto_cot=="Sí":                 sc2+=3
                if credinissan_cot=="Sí":           sc2+=5
                if hipotecario_cot=="Bancario":     sc2+=4
                elif hipotecario_cot=="Infonavit":  sc2+=2
                if tarjeta_alta_cot=="Sí":          sc2+=4
                if atrasos_cot=="Sin atrasos":      sc2+=5
                elif atrasos_cot=="1-30 días":      sc2+=2
                elif atrasos_cot=="31-60 días":     sc2-=4
                elif atrasos_cot=="61+ días":       sc2-=10

                cap_t  = (st.session_state.ingreso + ingreso_cot)*0.3
                men_g  = st.session_state.mensualidad
                buro_c = "BUENO" if sc2>=12 else ("REGULAR" if sc2>=6 else "MALO")

                if tipo_cot=="Conocido" and buro_c!="BUENO":
                    res_cot="❌ Debe ser línea directa con buen historial"
                elif cap_t>=men_g and buro_c=="BUENO":
                    res_cot="🟢 APROBADO FINAL"
                elif buro_c=="REGULAR":
                    res_cot="🟡 Aún condicionado — mejorar perfil"
                else:
                    res_cot="🔴 Cotitular no viable"

                st.session_state.cotitular_resultado = res_cot

        if st.session_state.cotitular_resultado:
            st.markdown(f"""
            <div class="result-card" style="margin-top:10px;">
              <div style="font-family:'Rajdhani',sans-serif;font-size:0.72rem;font-weight:700;
                  color:#38bdf8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:7px;">
                  Resultado cotitular</div>
              <div style="font-size:0.95rem;color:#e2e8f0;">{st.session_state.cotitular_resultado}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # PDF
        ok = all([r.get("asesor","").strip(), r.get("nombre","").strip(), r.get("telefono","").strip()])
        if not ok:
            st.warning("⚠️ Completa datos de asesor y cliente para generar PDF")
        else:
            buf = BytesIO()
            doc = SimpleDocTemplate(buf)
            sty = getSampleStyleSheet()
            content = [
                Paragraph("SOLICITUD DE PERFILAMIENTO CREDITICIO", sty["Title"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph(f"<b>Cliente:</b> {r.get('nombre','')}", sty["Normal"]),
                Paragraph(f"<b>Teléfono:</b> {r.get('telefono','')}", sty["Normal"]),
                Paragraph(f"<b>Correo:</b> {r.get('correo','')}", sty["Normal"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph("<b>RESULTADO DE PERFIL</b>", sty["Heading2"]),
                Paragraph(f"Estatus: {r['decision']}", sty["Normal"]),
                Paragraph(f"Probabilidad estimada: {r['prob']}%", sty["Normal"]),
                Paragraph(f"<b>Mensualidad estimada:</b> ${r.get('mensualidad',0):,.0f}", sty["Normal"]),
                Paragraph(f"<b>Capacidad de pago:</b> ${r.get('capacidad_pago',0):,.0f}", sty["Normal"]),
                Paragraph("<b>Análisis:</b>", sty["Heading3"]),
                Paragraph(r.get("mensaje_cliente",""), sty["Normal"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph("<b>Posibles validaciones:</b>", sty["Heading3"]),
                Paragraph("- Validación de ingresos\n- Confirmación de datos\n- Revisión por financiera", sty["Normal"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph("<b>ASEGURA TU UNIDAD</b>", sty["Heading2"]),
                Paragraph("Puedes iniciar tu trámite mediante apartado.", sty["Normal"]),
                Paragraph("Banco Principal BBVA: 012320001250476847", sty["Normal"]),
                Paragraph("Cuenta a nombre de DAOSA SA DE CV", sty["Normal"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph("<b>Contacto</b>", sty["Heading2"]),
                Paragraph(f"Asesor: {r.get('asesor','')}", sty["Normal"]),
                Paragraph(f"Teléfono: {r.get('telefono_asesor','')}", sty["Normal"]),
                Paragraph(f"Correo: {r.get('correo_asesor','')}", sty["Normal"]),
                Paragraph(f"RFC: {r.get('rfc','')}", sty["Normal"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph("<b>Nota:</b> La aprobación final dependerá de la evaluación de la financiera conforme a buró de crédito.", sty["Normal"]),
            ]
            doc.build(content)
            st.download_button("📄 Descargar PDF del perfil",
                data=buf.getvalue(), file_name="perfil_autoscore.pdf",
                mime="application/pdf", use_container_width=True)

        st.markdown('<div class="security-line">🛡️ Datos protegidos y seguros</div>', unsafe_allow_html=True)
