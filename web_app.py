import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="AutoScore AI", page_icon="🚗", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Exo+2:wght@300;400;500;600;700&display=swap');

/* ─── BASE ─────────────────────────────────── */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], section.main {
    background: #060d1c !important;
    color: #e2e8f0 !important;
}
[data-testid="stAppViewContainer"]::before {
    content: ""; position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(56,189,248,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,189,248,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none; z-index: 0;
}
[data-testid="stMain"]::before {
    content: ""; position: fixed; top: -150px; left: 50%;
    transform: translateX(-50%);
    width: 1400px; height: 400px;
    background: radial-gradient(ellipse, rgba(56,189,248,0.07) 0%, rgba(99,102,241,0.04) 40%, transparent 70%);
    filter: blur(60px); pointer-events: none; z-index: 0;
}
.block-container {
    position: relative; z-index: 1;
    padding: 0 1.5rem 2rem 1.5rem !important;
    max-width: 100% !important;
}
*, *::before, *::after {
    font-family: 'Exo 2', sans-serif !important;
    box-sizing: border-box;
}

/* ─── TOPBAR ─────────────────────────────────── */
.topbar-title {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.5rem; font-weight: 700;
    color: #e2e8f0; letter-spacing: 0.08em; line-height: 1;
}
.topbar-sub {
    color: #38bdf8; font-size: 0.65rem;
    letter-spacing: 0.16em; text-transform: uppercase; margin-top: 3px;
}
.topbar-divider {
    display: inline-block;
    width: 1px; height: 38px;
    background: rgba(56,189,248,0.2);
    margin: 0 16px; vertical-align: middle;
}
.topbar-desc {
    color: #334155; font-size: 0.7rem; letter-spacing: 0.04em;
}
.topbar-badge {
    background: rgba(56,189,248,0.07);
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 50px; padding: 4px 12px;
    font-size: 0.62rem; color: #38bdf8;
    letter-spacing: 0.1em; text-transform: uppercase; font-weight: 600;
}

/* ─── SECTION LABEL ─────────────────────────── */
.sec-label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.68rem; font-weight: 700;
    color: #38bdf8; text-transform: uppercase;
    letter-spacing: 0.14em; margin: 10px 0 5px;
    display: flex; align-items: center; gap: 7px;
    padding-bottom: 5px;
    border-bottom: 1px solid rgba(56,189,248,0.1);
}

/* ─── INPUTS compactos ───────────────────────── */
.stTextInput input, .stNumberInput input {
    background: rgba(3,9,22,0.92) !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(56,189,248,0.15) !important;
    border-radius: 8px !important;
    padding: 7px 12px !important;
    font-size: 0.82rem !important;
    width: 100% !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: rgba(56,189,248,0.55) !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,0.07) !important;
}
.stTextInput input::placeholder, .stNumberInput input::placeholder {
    color: #1e3a4a !important;
}
.stSelectbox > div > div {
    background: rgba(3,9,22,0.92) !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(56,189,248,0.15) !important;
    border-radius: 8px !important;
    padding: 2px 8px !important;
    font-size: 0.82rem !important;
}
label, [data-testid="stWidgetLabel"] p {
    color: #38bdf8 !important;
    font-size: 0.65rem !important; font-weight: 600 !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    margin-bottom: 2px !important;
}
.stNumberInput button {
    background: rgba(56,189,248,0.07) !important;
    border: 1px solid rgba(56,189,248,0.14) !important;
    color: #38bdf8 !important; border-radius: 6px !important;
    padding: 2px 8px !important; width: auto !important; margin: 0 !important;
}
div[data-testid="stVerticalBlock"] { gap: 0.28rem !important; }

/* ─── BOTÓN ──────────────────────────────────── */
.stFormSubmitButton > button, .stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 55%, #8b5cf6 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: 50px !important; padding: 12px 24px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem !important; font-weight: 700 !important;
    letter-spacing: 0.13em !important; text-transform: uppercase !important;
    box-shadow: 0 0 28px rgba(99,102,241,0.38), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    margin-top: 6px !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stFormSubmitButton > button:hover, .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 0 40px rgba(99,102,241,0.5) !important;
}

/* ─── EXPANDER — fix definitivo encimado ──────── */
[data-testid="stExpander"] {
    background: rgba(3,9,22,0.92) !important;
    border: 1px solid rgba(56,189,248,0.14) !important;
    border-radius: 10px !important;
    overflow: visible !important;
}
/* Header del expander */
[data-testid="stExpander"] details {
    background: transparent !important;
}
[data-testid="stExpander"] details summary {
    background: rgba(3,9,22,0.92) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    cursor: pointer !important;
    position: relative !important;
    z-index: 1 !important;
}
[data-testid="stExpander"] details summary::marker,
[data-testid="stExpander"] details summary::-webkit-details-marker {
    display: none !important;
    content: "" !important;
}
/* Texto del summary */
[data-testid="stExpander"] details summary p,
[data-testid="stExpander"] details summary div,
[data-testid="stExpander"] details summary span {
    color: #7dd3fc !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
/* Contenido expandido */
[data-testid="stExpander"] details > div {
    background: rgba(3,9,22,0.96) !important;
    border-top: 1px solid rgba(56,189,248,0.08) !important;
    padding: 12px 14px !important;
    border-radius: 0 0 10px 10px !important;
    position: relative !important;
    z-index: 0 !important;
}
[data-testid="stExpander"] details > div * {
    background: transparent !important;
    box-shadow: none !important;
}
/* Ícono flecha del expander */
[data-testid="stExpander"] svg {
    color: #7dd3fc !important;
    fill: #7dd3fc !important;
}

/* ─── ALERTS ──────────────────────────────────  */
.stSuccess > div { background:rgba(34,197,94,0.08)!important; border:1px solid rgba(34,197,94,0.28)!important; border-radius:9px!important; color:#86efac!important; font-size:0.82rem!important; }
.stWarning > div { background:rgba(245,158,11,0.07)!important; border:1px solid rgba(245,158,11,0.25)!important; border-radius:9px!important; color:#fcd34d!important; font-size:0.82rem!important; }
.stError   > div { background:rgba(239,68,68,0.07)!important;  border:1px solid rgba(239,68,68,0.25)!important;  border-radius:9px!important; color:#fca5a5!important; font-size:0.82rem!important; }
.stInfo    > div { background:rgba(56,189,248,0.06)!important; border:1px solid rgba(56,189,248,0.2)!important;  border-radius:9px!important; color:#7dd3fc!important;  font-size:0.82rem!important; }

hr { border:none!important; border-top:1px solid rgba(56,189,248,0.09)!important; margin:8px 0!important; }
.stCaption p { color:#f59e0b!important; font-size:0.72rem!important; }

.stLinkButton a {
    background:rgba(56,189,248,0.08)!important; border:1px solid rgba(56,189,248,0.22)!important;
    color:#7dd3fc!important; border-radius:8px!important; font-weight:600!important;
    font-size:0.8rem!important; width:100%!important; display:block!important;
    text-align:center!important; padding:9px!important;
}
.stDownloadButton > button {
    background:rgba(56,189,248,0.08)!important; border:1px solid rgba(56,189,248,0.22)!important;
    color:#7dd3fc!important; border-radius:8px!important; font-weight:600!important;
    font-size:0.8rem!important; width:100%!important; padding:9px!important;
}

/* ─── RESULTADO UI ────────────────────────────── */

/* PROBABILIDAD GRANDE */
.prob-hero {
    display: flex; align-items: flex-end; gap: 10px;
    padding: 16px 20px 12px;
    background: linear-gradient(135deg, rgba(8,18,40,0.98), rgba(4,10,24,0.99));
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 14px; margin-bottom: 10px;
    position: relative; overflow: hidden;
}
.prob-hero::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #38bdf8, #6366f1, #8b5cf6);
}
.prob-number {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 3.8rem; font-weight: 700; line-height: 1;
}
.prob-label {
    font-size: 0.7rem; color: #475569; text-transform: uppercase;
    letter-spacing: 0.1em; margin-bottom: 8px;
}
.prob-sublabel {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.82rem; color: #64748b; letter-spacing: 0.04em;
}

/* SCORE BADGE */
.score-badge {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 10px 16px; border-radius: 12px;
    margin: 6px 0; width: 100%;
}
.score-badge .score-em  { font-size: 1.5rem; }
.score-badge .score-lbl {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem; font-weight: 700; letter-spacing: 0.06em;
}
.score-badge .score-sub { font-size: 0.72rem; color: #64748b; margin-top: 1px; }

/* MÉTRICAS 2 COL */
.metrics-2 { display: flex; gap: 10px; margin: 8px 0; }
.metric-tile {
    flex: 1; border-radius: 10px; padding: 10px 14px;
}
.metric-tile.blue   { background:rgba(56,189,248,0.07); border:1px solid rgba(56,189,248,0.16); }
.metric-tile.purple { background:rgba(99,102,241,0.07); border:1px solid rgba(99,102,241,0.16); }
.metric-tile .mt-lbl {
    font-size: 0.62rem; text-transform: uppercase;
    letter-spacing: 0.08em; margin-bottom: 4px; font-weight: 600;
}
.metric-tile.blue   .mt-lbl { color: #7dd3fc; }
.metric-tile.purple .mt-lbl { color: #a5b4fc; }
.metric-tile .mt-val {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.35rem; font-weight: 700; color: #e2e8f0; line-height: 1;
}

/* SEMÁFORO DECISIÓN */
.semaforo {
    display: flex; align-items: center; justify-content: center;
    gap: 10px; padding: 10px 16px; border-radius: 10px;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase; margin: 8px 0;
}
.semaforo.verde    { background:rgba(34,197,94,0.11);  border:1px solid rgba(34,197,94,0.3);  color:#4ade80; }
.semaforo.amarillo { background:rgba(234,179,8,0.09);  border:1px solid rgba(234,179,8,0.26); color:#facc15; }
.semaforo.naranja  { background:rgba(249,115,22,0.09); border:1px solid rgba(249,115,22,0.26);color:#fb923c; }
.semaforo.rojo     { background:rgba(239,68,68,0.09);  border:1px solid rgba(239,68,68,0.26); color:#f87171; }

/* MSG CLIENTE */
.msg-cliente {
    background: rgba(56,189,248,0.05);
    border: 1px solid rgba(56,189,248,0.12);
    border-left: 3px solid #38bdf8;
    border-radius: 0 9px 9px 0;
    padding: 10px 14px; color: #cbd5e1;
    font-size: 0.8rem; line-height: 1.6; margin: 6px 0;
}

/* ESTRATEGIA INTERNA */
.estrategia-box {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.18);
    border-left: 3px solid #ef4444;
    border-radius: 0 9px 9px 0;
    padding: 10px 14px; color: #fca5a5;
    font-size: 0.78rem; line-height: 1.6;
}

/* ALERTA CHIP */
.alerta-chip {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 11px; border-radius: 7px;
    font-size: 0.74rem; font-weight: 600;
    margin: 3px 0; letter-spacing: 0.02em;
}
.alerta-chip.warn { background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2); color:#fcd34d; }
.alerta-chip.ok   { background:rgba(34,197,94,0.06);  border:1px solid rgba(34,197,94,0.16); color:#86efac; }
.alerta-chip.bad  { background:rgba(239,68,68,0.08);  border:1px solid rgba(239,68,68,0.2);  color:#fca5a5; }

/* CONDICIONAMIENTOS */
.cond-box {
    background: rgba(234,179,8,0.07);
    border: 1px solid rgba(234,179,8,0.22);
    border-radius: 9px; padding: 10px 14px;
    color: #fde68a; font-size: 0.76rem;
    line-height: 1.75; margin: 4px 0; font-weight: 500;
}

/* CUENTA */
.cuenta-box {
    background: rgba(8,18,38,0.9);
    border: 1px solid rgba(56,189,248,0.14);
    border-radius: 9px; padding: 10px 14px; margin: 4px 0;
}

.security-line {
    text-align:center; color:#1e3a4a; font-size:0.68rem; letter-spacing:0.06em;
    margin-top:8px; display:flex; align-items:center; justify-content:center; gap:5px;
}

/* separador vertical panel */
.panel-left  { border-right: 1px solid rgba(56,189,248,0.09); padding-right: 16px; }
.panel-right { padding-left: 16px; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────
for k, v in {
    "resultado": None, "cotitular_activo": False,
    "cotitular_resultado": None, "ingreso": 0.0, "mensualidad": 0.0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── TOPBAR — título centrado, sin imagen problemática ──────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;padding:10px 0 8px;">
  <div>
    <div class="topbar-title">AutoScore AI</div>
    <div class="topbar-sub">Aprobación Inteligente</div>
  </div>
  <span class="topbar-divider"></span>
  <div class="topbar-desc">Herramienta de Pre-Análisis de Crédito Automotriz</div>
  <div style="margin-left:auto;">
    <span class="topbar-badge">🔒 Datos protegidos</span>
  </div>
</div>
<div style="height:1px;margin:2px 0 14px;
background:linear-gradient(90deg,transparent,#38bdf8 25%,#8b5cf6 75%,transparent);
box-shadow:0 0 14px rgba(56,189,248,0.28);"></div>
""", unsafe_allow_html=True)

# ── DOS COLUMNAS ───────────────────────────────────────────────────
col_izq, col_der = st.columns([1, 1], gap="medium")

# ╔══════════════════════════════════╗
# ║      IZQUIERDA — FORMULARIO      ║
# ╚══════════════════════════════════╝
with col_izq:

    # LOGO arriba del formulario — izquierda
    _lc1, _lc2, _lc3 = st.columns([1, 2, 1])
    with _lc2:
        st.image("logo_new.png", use_container_width=True)

    st.markdown("<div style='margin:2px 0 10px'></div>", unsafe_allow_html=True)

    with st.form("formulario"):

        # ASESOR — ahora dentro del form para alineación consistente
        st.markdown('<div class="sec-label">👤 Datos del Asesor</div>', unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        with a1: asesor = st.text_input("Nombre asesor", placeholder="Nombre completo")
        with a2: rfc    = st.text_input("RFC asesor", placeholder="XAXX010101000")
        b1, b2 = st.columns(2)
        with b1: telefono_asesor = st.text_input("Teléfono asesor", placeholder="55 1234 5678")
        with b2: correo_asesor   = st.text_input("Correo asesor", placeholder="asesor@correo.com")

        # CLIENTE
        st.markdown('<div class="sec-label">👥 Datos del Cliente</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: nombre_cliente = st.text_input("Nombre cliente", placeholder="Nombre completo")
        with c2: telefono       = st.text_input("Teléfono", placeholder="55 9876 5432")
        correo = st.text_input("Correo cliente", placeholder="cliente@correo.com")

        # PERFIL
        st.markdown('<div class="sec-label">📊 Perfil Financiero</div>', unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)
        with p1: edad        = st.number_input("Edad", 18, 73, 18)
        with p2: ingreso     = st.number_input("Ingreso mensual ($)", min_value=6500.0, value=6500.0, step=500.0, format="%.0f")
        with p3: tipo_ingreso= st.selectbox("Tipo de ingreso", ["Nómina","Independiente","No comprueba"])

        q1, q2, q3 = st.columns(3)
        with q1: negocio_casa  = st.selectbox("Negocio en domicilio", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        with q2: domicilio     = st.selectbox("Antigüedad domicilio", [1,2,3], format_func=lambda x:["<1 año","1-3 años","+3 años"][x-1])
        with q3: domicilio_buro= st.selectbox("Domicilio = ID", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        if tipo_ingreso == "Independiente":
            st.caption("⚠️ Solo aplica para independientes")

        # VEHÍCULO
        st.markdown('<div class="sec-label">🚗 Datos del Vehículo</div>', unsafe_allow_html=True)
        v1, v2, v3, v4 = st.columns(4)
        with v1: precio    = st.number_input("Precio ($)", min_value=0.0, format="%0.0f")
        with v2: enganche  = st.number_input("Enganche ($)", min_value=0.0, format="%0.0f")
        with v3: plazo     = st.selectbox("Plazo", [12,24,36,48,60,72])
        with v4: consultas = st.number_input("Consultas buró", 0, 20)

        # HISTORIAL
        st.markdown('<div class="sec-label">🏦 Historial Crediticio</div>', unsafe_allow_html=True)
        h1, h2, h3 = st.columns(3)
        with h1: auto        = st.selectbox("Crédito auto previo", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        with h2: credinissan = st.selectbox("CrediNissan", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        with h3: hipotecario = st.selectbox("Hipotecario", [1,2,3], format_func=lambda x:["Bancario","Infonavit","No tiene"][x-1])

        i1, i2, i3 = st.columns(3)
        with i1: tarjeta_alta = st.selectbox("Tarjetas >$100K", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        with i2: tarjeta_baja = st.selectbox("Tarjetas <$100K", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        with i3: atrasos      = st.selectbox("Atrasos en buró", [1,2,3], format_func=lambda x:["1-30d","31-60d","+61d"][x-1])

        # PERFIL COMPRA
        st.markdown('<div class="sec-label">🔥 Perfil de Compra</div>', unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: enganche_disp = st.selectbox("¿Tiene enganche?", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        with k2: compra_mes    = st.selectbox("¿Compra este mes?", [1,2], format_func=lambda x:"Sí" if x==1 else "No")
        with k3: unidad        = st.selectbox("¿Hay unidad?", [1,2], format_func=lambda x:"Sí" if x==1 else "No")

        st.markdown("<div style='margin:4px 0'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✦  ANALIZAR PERFIL FINANCIERO")

# ── LÓGICA ─────────────────────────────────────────────────────────
if submitted:
    st.session_state.ingreso = ingreso
    monto       = max(precio - enganche, 0)
    tasa_m      = 0.015
    mensualidad = (monto*(tasa_m*(1+tasa_m)**plazo)/((1+tasa_m)**plazo-1)) if plazo>0 and monto>0 else 0
    st.session_state.mensualidad = mensualidad
    enganche_pct = (enganche/precio)*100 if precio>0 else 0

    riesgo_alto = riesgo_medio = False
    if atrasos==3:                              riesgo_alto=True
    if consultas>=8:                            riesgo_alto=True
    elif consultas>=5:                          riesgo_medio=True
    if tipo_ingreso=="Independiente":           riesgo_medio=True
    if tipo_ingreso=="No comprueba":            riesgo_alto=True
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

    # FIX: score_color se asigna DESPUÉS de calcular la probabilidad final
    # para que refleje el prob real, no el perfil base
    if prob>=80:   sc="AZUL"
    elif prob>=70: sc="VERDE"
    elif prob>=45: sc="AMARILLO"
    elif prob>=35: sc="NARANJA"
    else:          sc="ROJO"

    msg_c=msg_a=""; decision="EN EVALUACIÓN"; plan="REVISION"
    condicionamientos=[]

    if consultas>=10:
        decision="ESTRATEGIA ALTERNATIVA"; plan="COTITULAR"
        condicionamientos.append("COTITULAR OBLIGATORIO")
    elif riesgo_alto and perfil!="FUERTE":
        decision="ESTRATEGIA ALTERNATIVA"; plan="ALTERNATIVA"
        msg_c="Tu perfil puede avanzar mediante una alternativa de financiamiento."
        msg_a="Riesgo alto: subir enganche ≥10% / comprobar ingresos / buscar cotitular."
        condicionamientos+=["SUBIR ENGANCHE","COMPROBAR INGRESOS","COTITULAR"]
    elif atrasos==3:
        decision="ESTRATEGIA ALTERNATIVA"; plan="ALTERNATIVA"
        msg_c="Tu perfil puede avanzar mediante una alternativa de financiamiento."
        msg_a="Subir enganche / cotitular / evitar consultas."
        condicionamientos+=["SUBIR ENGANCHE","COTITULAR","EVITAR CONSULTAS"]
    elif sc=="ROJO":
        decision="ESTRATEGIA ALTERNATIVA"; plan="COTITULAR"
        msg_c="Tu perfil actualmente requiere una alternativa de financiamiento."
        msg_a="Cotitular fuerte / Subir enganche / Evitar consultas en buró."
        condicionamientos+=["COTITULAR FUERTE","MAYOR ENGANCHE"]
    elif excede and prob<70:
        decision="AJUSTE NECESARIO"; plan="AJUSTAR_PLAZO"
        msg_c="La mensualidad puede ajustarse para mejorar tu perfil."
        msg_a="Ampliar plazo / Reducir monto / Validar ingresos."
        condicionamientos+=["AMPLIAR PLAZO","VALIDAR INGRESOS"]
    elif riesgo_medio and prob<60:
        decision="PERFIL CON OPORTUNIDAD"; plan="RESCATE"
        msg_c="Tu perfil tiene alta posibilidad de avanzar ajustando puntos clave."
        msg_a="Enganche ≥25% / Cotitular línea directa / Evitar más consultas."
        condicionamientos+=["MAYOR ENGANCHE","COTITULAR","COMPROBAR INGRESOS Y/O INVESTIGACIÓN FÍSICA"]
    elif prob>=70:
        if riesgo_medio:
            decision="APROBADO EN ANÁLISIS DE FINANCIERA"; plan="SE VA A ANALISIS"
            msg_c="Tu perfil es viable y puede avanzar a proceso de aprobación."
            msg_a="Validación de ingresos / Investigación telefónica."
            condicionamientos+=["VALIDACIÓN DE INGRESOS","INVESTIGACIÓN TELEFÓNICA"]
        else:
            decision="APROBADO"; plan="AUTOMATICO"
            msg_c="Tu perfil cumple los criterios para avanzar en automático."
            msg_a="Perfil limpio. Proceder directo."
    elif prob>=50:
        if enganche_pct<20 or riesgo_medio:
            decision="APROBABLE CON AJUSTES"; plan="CONDICIONADO"
            msg_c="Tu perfil es viable realizando algunos ajustes."
            msg_a="Subir enganche +15pts / Validación por financiera."
            condicionamientos+=["MAYOR ENGANCHE","VALIDACIÓN FINANCIERA"]
        else:
            decision="PRE APROBADO"; plan="DIRECTO"
            msg_c="Tu perfil es favorable para avanzar."
            msg_a="Perfil estable. Proceder."
    elif prob>=35:
        decision="PERFIL MEJORABLE"; plan="COTITULAR"
        msg_c="Tu perfil puede fortalecerse con apoyo adicional."
        msg_a="Cotitular fuerte / Comprobar ingresos / Mejorar enganche."
        condicionamientos+=["COTITULAR","COMPROBAR INGRESOS","MEJORAR ENGANCHE"]
    else:
        decision="ESTRATEGIA ALTERNATIVA"; plan="ALTERNATIVA"
        msg_c="Tu perfil puede avanzar mediante una alternativa de financiamiento."
        msg_a="Financiera flexible / Reestructura de perfil."
        condicionamientos+=["FINANCIERA FLEXIBLE","REESTRUCTURA DE PERFIL"]

    alerta_cotitular     = "COTITULAR" in " ".join(condicionamientos)
    alerta_ingresos      = any(x in " ".join(condicionamientos) for x in ["INGRESO","INGRESOS","VALIDACIÓN"])
    alerta_investigacion = "INVESTIGACIÓN" in " ".join(condicionamientos) or "FÍSICA" in " ".join(condicionamientos)

    inv="Sin alerta relevante"
    if tipo_ingreso!="Nómina" and prob<45:     inv="Validación adicional requerida"
    if domicilio_buro==2:                      inv="Validación de domicilio"
    if tipo_ingreso=="Independiente":          inv="Validación de ingresos"
    if tipo_ingreso=="Independiente" and negocio_casa==1:
        prob=max(prob,80); inv="Requiere validación física"

    docs=["INE","Comprobante de domicilio"]
    if plan=="DIRECTO":          docs=["INE","Comprobante","Cotización"]
    elif plan=="COTITULAR":      docs+=["Cotitular obligatorio"]
    elif tipo_ingreso=="Nómina": docs+=["Nómina","Estado de cuenta"]
    else:                        docs+=["Estados de cuenta"]

    if plan in ["AUTOMATICO","DIRECTO"]:             financiera="Automático"
    elif plan in ["SE VA A ANALISIS","CONDICIONADO"]: financiera="Condicionado"
    else:                                            financiera="Revisión especial"

    # semaforo
    if "APROBADO" in decision and "FINANCIERA" not in decision: sem="verde"
    elif "FINANCIERA" in decision or "PRE" in decision:          sem="amarillo"
    elif "ALTERNATIVA" in decision:                              sem="rojo"
    else:                                                        sem="naranja"

    # color prob
    if prob>=70:   prob_col="#4ade80"
    elif prob>=50: prob_col="#facc15"
    elif prob>=35: prob_col="#fb923c"
    else:          prob_col="#f87171"

    st.session_state.resultado = {
        "sc":sc, "prob":prob, "prob_col":prob_col, "sem":sem,
        "temp":temp, "inv":inv, "decision":decision,
        "plan":plan, "msg_c":msg_c, "msg_a":msg_a,
        "condicionamientos":condicionamientos,
        "alerta_cotitular":alerta_cotitular,
        "alerta_ingresos":alerta_ingresos,
        "alerta_investigacion":alerta_investigacion,
        "financiera":financiera, "perfil":perfil, "score":score,
        "enganche_pct":enganche_pct,
        "nombre":nombre_cliente, "telefono":telefono, "correo":correo,
        "asesor":asesor, "telefono_asesor":telefono_asesor,
        "correo_asesor":correo_asesor, "rfc":rfc,
        "docs":docs, "mensualidad":mensualidad, "cap_pago":cap_pago,
    }
    st.session_state.cotitular_activo    = (plan=="COTITULAR")
    st.session_state.cotitular_resultado = None

# ╔══════════════════════════════════════╗
# ║   DERECHA — RESULTADO REESTRUCTURADO ║
# ╚══════════════════════════════════════╝
with col_der:

    if not st.session_state.resultado:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;
            justify-content:center;min-height:55vh;gap:12px;opacity:0.28;">
          <div style="font-size:3.2rem;">📊</div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:0.82rem;color:#38bdf8;
              text-transform:uppercase;letter-spacing:0.12em;text-align:center;line-height:1.8;">
              Resultado del Análisis<br>
              <span style="font-size:0.62rem;opacity:0.7;">Completa el formulario y presiona Analizar</span>
          </div>
        </div>""", unsafe_allow_html=True)

    else:
        r = st.session_state.resultado

        SCORE_MAP = {
            "AZUL":     ("🔵","SCORE AZUL",    "#38bdf8","Perfil fuerte — alta probabilidad de aprobación"),
            "VERDE":    ("🟢","SCORE VERDE",   "#22c55e","Buen perfil — condiciones normales"),
            "AMARILLO": ("🟡","SCORE AMARILLO","#eab308","Perfil medio — requiere validación adicional"),
            "NARANJA":  ("🟠","SCORE NARANJA", "#f97316","Perfil con áreas de oportunidad"),
            "ROJO":     ("🔴","SCORE ROJO",    "#ef4444","Perfil requiere estrategia alternativa"),
        }
        em, lbl, col_hex, dsc = SCORE_MAP[r["sc"]]

        # ── 1. DECISIÓN — lo primero y más grande ─────────────
        sem_icon = {'verde':'✅','amarillo':'⚡','naranja':'⚠️','rojo':'🔴'}[r['sem']]
        st.markdown(f"""
        <div class="prob-hero">
          <div style="flex:1;">
            <div class="prob-label">Resultado del análisis</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.6rem;font-weight:700;
                line-height:1.1;margin:4px 0 6px;color:{'#4ade80' if r['sem']=='verde' else '#facc15' if r['sem']=='amarillo' else '#fb923c' if r['sem']=='naranja' else '#f87171'};">
                {sem_icon} {r['decision']}
            </div>
            <div class="prob-sublabel">{r['temp']} &nbsp;·&nbsp; {r['financiera']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 2. MENSAJE CLIENTE ────────────────────────────────
        if r.get("msg_c"):
            st.markdown(f'<div class="msg-cliente">💡 {r["msg_c"]}</div>', unsafe_allow_html=True)

        # ── 3. PROBABILIDAD + SCORE ───────────────────────────
        rgb = {'AZUL':'56,189,248','VERDE':'34,197,94','AMARILLO':'234,179,8','NARANJA':'249,115,22','ROJO':'239,68,68'}[r['sc']]
        st.markdown(f"""
        <div class="metrics-2" style="margin-top:10px;">
          <div class="metric-tile blue" style="text-align:center;">
            <div class="mt-lbl">Probabilidad de aprobación</div>
            <div class="mt-val" style="color:{r['prob_col']};font-size:2.2rem;">{r['prob']}%</div>
          </div>
          <div class="metric-tile" style="background:rgba({rgb},0.08);border:1px solid {col_hex}33;text-align:center;">
            <div class="mt-lbl" style="color:{col_hex};">Score crediticio</div>
            <div style="font-size:1.6rem;line-height:1.2;margin:4px 0;">{em}</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:0.88rem;font-weight:700;color:{col_hex};">{lbl}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 4. MENSUALIDAD + CAPACIDAD ────────────────────────
        excede_color = "#f87171" if r["mensualidad"] > r["cap_pago"] else "#e2e8f0"
        st.markdown(f"""
        <div class="metrics-2">
          <div class="metric-tile blue">
            <div class="mt-lbl">Capacidad de pago</div>
            <div class="mt-val">${r['cap_pago']:,.0f}</div>
          </div>
          <div class="metric-tile purple">
            <div class="mt-lbl">Mensualidad estimada</div>
            <div class="mt-val" style="color:{excede_color};">${r['mensualidad']:,.0f}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 5. ALERTAS ────────────────────────────────────────
        st.markdown('<div class="sec-label">⚠️ Riesgos detectados</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="alerta-chip {'bad' if r['alerta_cotitular'] else 'ok'}">
            {'🔴' if r['alerta_cotitular'] else '🟢'} COTITULAR &nbsp;—&nbsp;
            {'Requiere cotitular' if r['alerta_cotitular'] else 'Sin alerta'}
        </div>
        <div class="alerta-chip {'bad' if r['alerta_ingresos'] else 'ok'}">
            {'🔴' if r['alerta_ingresos'] else '🟢'} INGRESOS &nbsp;—&nbsp;
            {'Validar ingresos' if r['alerta_ingresos'] else 'Sin alerta'}
        </div>
        <div class="alerta-chip {'bad' if r['alerta_investigacion'] else 'ok'}">
            {'🔴' if r['alerta_investigacion'] else '🟢'} INVESTIGACIÓN &nbsp;—&nbsp; {r['inv']}
        </div>
        """, unsafe_allow_html=True)

        # ── 6. ESTRATEGIA INTERNA — toggle manual (sin st.expander) ──
        if "mostrar_estrategia" not in st.session_state:
            st.session_state.mostrar_estrategia = False

        lbl_btn = "🔓 Ocultar estrategia interna" if st.session_state.mostrar_estrategia else "🔒 Ver estrategia interna — solo asesor"
        if st.button(lbl_btn, key="btn_estrategia"):
            st.session_state.mostrar_estrategia = not st.session_state.mostrar_estrategia

        if st.session_state.mostrar_estrategia:
            st.markdown(f"""
            <div class="estrategia-box">
                🔴 {r["msg_a"]}<br><br>
                <b>Nivel interno:</b> {r["perfil"]} &nbsp;·&nbsp;
                Score: {r["score"]} pts &nbsp;·&nbsp;
                Enganche: {r["enganche_pct"]:.0f}%
            </div>
            """, unsafe_allow_html=True)

        # ── 7. CONDICIONAMIENTOS ──────────────────────────────
        if r["condicionamientos"]:
            st.markdown('<div class="sec-label">📋 Condicionamientos</div>', unsafe_allow_html=True)
            cond_items = "".join([f"• {c}<br>" for c in r["condicionamientos"]])
            st.markdown(f'<div class="cond-box">{cond_items}</div>', unsafe_allow_html=True)

        # ── 8. DOCUMENTACIÓN ─────────────────────────────────
        st.markdown('<div class="sec-label">📄 Documentación requerida</div>', unsafe_allow_html=True)
        docs_chips = " &nbsp;·&nbsp; ".join([f"📎 {d}" for d in r["docs"]])
        st.markdown(f'<div style="color:#64748b;font-size:0.76rem;padding:4px 2px;">{docs_chips}</div>', unsafe_allow_html=True)

        # ── 9. SIGUIENTE PASO + CUENTA ────────────────────────
        st.markdown('<div class="sec-label">💰 Siguiente paso</div>', unsafe_allow_html=True)
        anticipo = "Solicitar ENGANCHE COMPLETO" if r["plan"]=="DIRECTO" else "Solicitar APARTADO $5,000"
        st.markdown(f"""
        <div class="cuenta-box">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;">
            <div>
              <div style="color:#fcd34d;font-size:0.78rem;font-weight:700;margin-bottom:6px;">👉 {anticipo}</div>
              <div style="font-family:'Rajdhani',sans-serif;font-size:0.88rem;font-weight:700;color:#e2e8f0;">DAOSA SA DE CV — BBVA</div>
              <div style="color:#475569;font-size:0.75rem;margin-top:2px;letter-spacing:0.03em;">012320001250476847</div>
            </div>
            <div style="color:#ef4444;font-size:0.7rem;font-weight:600;text-align:right;
                line-height:1.5;padding:4px 0;">⚠️ Solicita anticipo<br>para asegurar unidad</div>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin:6px 0'></div>", unsafe_allow_html=True)
        st.link_button("📊 Abrir Cotizador",
            "https://procotiza.losnrtelepro.com.mx/Procotiza/login.aspx?mns",
            use_container_width=True)

        # ── COTITULAR ─────────────────────────────────────────
        if st.session_state.cotitular_activo:
            st.markdown('<div class="sec-label">👥 Análisis de Cotitular</div>', unsafe_allow_html=True)
            with st.form("formulario_cotitular"):
                ct1, ct2 = st.columns(2)
                with ct1: tipo_cot    = st.selectbox("Tipo", ["Línea directa","Conocido"])
                with ct2: ingreso_cot = st.number_input("Ingreso cotitular ($)", min_value=0.0, step=500.0)
                cu1,cu2,cu3 = st.columns(3)
                with cu1: auto_cot         = st.selectbox("Auto previo",  ["Sí","No"])
                with cu2: credinissan_cot  = st.selectbox("CrediNissan",   ["Sí","No"])
                with cu3: hipotecario_cot  = st.selectbox("Hipotecario",   ["No tiene","Infonavit","Bancario"])
                cv1,cv2 = st.columns(2)
                with cv1: tarjeta_alta_cot = st.selectbox("Tarjetas >100K",["Sí","No"])
                with cv2: atrasos_cot      = st.selectbox("Buró",["Sin atrasos","1-30d","31-60d","61+d"])
                submit_cot = st.form_submit_button("✦  EVALUAR COTITULAR")

            if submit_cot:
                sc2=0
                if auto_cot=="Sí":                 sc2+=3
                if credinissan_cot=="Sí":           sc2+=5
                if hipotecario_cot=="Bancario":     sc2+=4
                elif hipotecario_cot=="Infonavit":  sc2+=2
                if tarjeta_alta_cot=="Sí":          sc2+=4
                if atrasos_cot=="Sin atrasos":      sc2+=5
                elif atrasos_cot=="1-30d":          sc2+=2
                elif atrasos_cot=="31-60d":         sc2-=4
                elif atrasos_cot=="61+d":           sc2-=10
                cap_t  = (st.session_state.ingreso + ingreso_cot)*0.3
                men_g  = st.session_state.mensualidad
                buro_c = "BUENO" if sc2>=12 else ("REGULAR" if sc2>=6 else "MALO")
                if tipo_cot=="Conocido" and buro_c!="BUENO":   res_cot="❌ Debe ser línea directa con buen historial"
                elif cap_t>=men_g and buro_c=="BUENO":         res_cot="🟢 APROBADO FINAL"
                elif buro_c=="REGULAR":                        res_cot="🟡 Aún condicionado — mejorar perfil"
                else:                                          res_cot="🔴 Cotitular no viable"
                st.session_state.cotitular_resultado = res_cot

        if st.session_state.cotitular_resultado:
            st.markdown(f"""
            <div class="alerta-chip {'ok' if 'APROBADO' in st.session_state.cotitular_resultado else 'bad'}"
                style="margin-top:4px;font-size:0.82rem;">
                {st.session_state.cotitular_resultado}
            </div>""", unsafe_allow_html=True)

        # ── PDF ───────────────────────────────────────────────
        st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)
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
                Paragraph(f"Probabilidad de aprobación: {r['prob']}%", sty["Normal"]),
                Paragraph(f"Score crediticio: {lbl}", sty["Normal"]),
                Paragraph(f"Estatus: {r['decision']}", sty["Normal"]),
                Paragraph(f"Mensualidad estimada: ${r.get('mensualidad',0):,.0f}", sty["Normal"]),
                Paragraph(f"Capacidad de pago: ${r.get('cap_pago',0):,.0f}", sty["Normal"]),
                Paragraph(f"Condicionamientos: {', '.join(r.get('condicionamientos',[]))}", sty["Normal"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph(r.get("msg_c",""), sty["Normal"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph("<b>ASEGURA TU UNIDAD</b>", sty["Heading2"]),
                Paragraph("BBVA · DAOSA SA DE CV · 012320001250476847", sty["Normal"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph("<b>Contacto</b>", sty["Heading2"]),
                Paragraph(f"Asesor: {r.get('asesor','')}", sty["Normal"]),
                Paragraph(f"Teléfono: {r.get('telefono_asesor','')}", sty["Normal"]),
                Paragraph(f"Correo: {r.get('correo_asesor','')}", sty["Normal"]),
                Paragraph(f"RFC: {r.get('rfc','')}", sty["Normal"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph("La aprobación final dependerá de la evaluación de la financiera conforme a buró de crédito.", sty["Normal"]),
            ]
            doc.build(content)
            st.download_button("📄 Descargar PDF del perfil",
                data=buf.getvalue(), file_name="perfil_autoscore.pdf",
                mime="application/pdf", use_container_width=True)

        st.markdown('<div class="security-line">🛡️ Datos protegidos y seguros</div>', unsafe_allow_html=True)
