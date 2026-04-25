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

/* ─── TOPBAR ────────────────────────────────── */
.topbar {
    display: flex; align-items: center; gap: 0;
    padding: 10px 0 10px 0;
    border-bottom: 1px solid rgba(56,189,248,0.15);
    margin-bottom: 16px;
    position: relative;
}
.topbar-logo { display:flex; align-items:center; }
.topbar-divider {
    width: 1px; height: 44px;
    background: rgba(56,189,248,0.2);
    margin: 0 18px;
}
.topbar-title {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.5rem; font-weight: 700;
    color: #e2e8f0; letter-spacing: 0.08em;
    line-height: 1;
}
.topbar-sub {
    color: #38bdf8; font-size: 0.65rem;
    letter-spacing: 0.16em; text-transform: uppercase; margin-top: 3px;
}
.topbar-badge {
    margin-left: auto;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 50px; padding: 5px 14px;
    font-size: 0.65rem; color: #38bdf8;
    letter-spacing: 0.1em; text-transform: uppercase;
    font-weight: 600;
}

/* ─── PANEL SEPARADOR ───────────────────────── */
.panel-left  { border-right: 1px solid rgba(56,189,248,0.1); padding-right: 18px; }
.panel-right { padding-left: 18px; }

/* ─── SECTION LABEL ─────────────────────────── */
.sec-label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.7rem; font-weight: 700;
    color: #38bdf8; text-transform: uppercase;
    letter-spacing: 0.14em; margin: 12px 0 6px;
    display: flex; align-items: center; gap: 7px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(56,189,248,0.1);
}

/* ─── ROW TABLE (estilo Excel) ───────────────── */
.row-table { width: 100%; margin-bottom: 2px; }
.row-table .row {
    display: flex; align-items: center;
    padding: 5px 10px;
    border-bottom: 1px solid rgba(56,189,248,0.05);
    gap: 8px;
}
.row-table .row:hover { background: rgba(56,189,248,0.03); }
.row-table .row .lbl {
    flex: 0 0 52%; color: #64748b;
    font-size: 0.76rem; letter-spacing: 0.02em;
}
.row-table .row .val {
    flex: 1; color: #cbd5e1;
    font-size: 0.76rem; font-weight: 600;
    text-align: right;
}
.val.green  { color: #4ade80 !important; }
.val.yellow { color: #facc15 !important; }
.val.red    { color: #f87171 !important; }
.val.blue   { color: #38bdf8 !important; }
.val.orange { color: #fb923c !important; }

/* ─── RESULTADO HEADER ───────────────────────── */
.res-header {
    display: flex; align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    background: rgba(56,189,248,0.06);
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 10px; margin-bottom: 10px;
}
.res-title {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem; font-weight: 700;
    color: #7dd3fc; text-transform: uppercase; letter-spacing: 0.1em;
}
.res-pct {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.6rem; font-weight: 700; line-height: 1;
}

/* ─── SEMÁFORO ───────────────────────────────── */
.semaforo {
    display: flex; align-items: center; justify-content: center;
    gap: 10px; padding: 9px 14px; border-radius: 8px;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin: 4px 0;
}
.semaforo.verde   { background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.3); color:#4ade80; }
.semaforo.amarillo{ background:rgba(234,179,8,0.10); border:1px solid rgba(234,179,8,0.28); color:#facc15; }
.semaforo.naranja { background:rgba(249,115,22,0.10); border:1px solid rgba(249,115,22,0.28); color:#fb923c; }
.semaforo.rojo    { background:rgba(239,68,68,0.10); border:1px solid rgba(239,68,68,0.28); color:#f87171; }

/* ─── ALERTA CHIP ────────────────────────────── */
.alerta-chip {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 11px; border-radius: 7px;
    font-size: 0.74rem; font-weight: 600;
    margin: 4px 0; letter-spacing: 0.03em;
}
.alerta-chip.warn { background:rgba(245,158,11,0.09); border:1px solid rgba(245,158,11,0.22); color:#fcd34d; }
.alerta-chip.ok   { background:rgba(34,197,94,0.07);  border:1px solid rgba(34,197,94,0.18);  color:#86efac; }
.alerta-chip.bad  { background:rgba(239,68,68,0.09);  border:1px solid rgba(239,68,68,0.22);  color:#fca5a5; }

/* ─── CONDICIONAMIENTOS BOX ──────────────────── */
.cond-box {
    background: rgba(234,179,8,0.08);
    border: 1px solid rgba(234,179,8,0.25);
    border-radius: 9px; padding: 10px 14px;
    color: #fde68a; font-size: 0.78rem;
    line-height: 1.7; margin: 6px 0;
    font-weight: 500;
}

/* ─── ESTRATEGIA INTERNA ─────────────────────── */
.estrategia-box {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.18);
    border-left: 3px solid #ef4444;
    border-radius: 0 9px 9px 0;
    padding: 10px 14px; color: #fca5a5;
    font-size: 0.78rem; line-height: 1.65;
    margin: 4px 0;
}

/* ─── CUENTA BOX ────────────────────────────── */
.cuenta-box {
    background: rgba(8,18,38,0.9);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 9px; padding: 10px 14px; margin: 6px 0;
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
div[data-testid="stVerticalBlock"] { gap: 0.3rem !important; }

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

/* ─── EXPANDER oscuro ────────────────────────── */
details, summary,
[data-testid="stExpander"],
[data-testid="stExpander"] > div,
.streamlit-expanderHeader,
.streamlit-expanderContent {
    background: rgba(3,9,22,0.88) !important;
    border: 1px solid rgba(56,189,248,0.13) !important;
    border-radius: 9px !important; color: #7dd3fc !important;
}
.streamlit-expanderHeader p, [data-testid="stExpander"] summary p {
    color: #7dd3fc !important; font-size: 0.78rem !important; font-weight: 600 !important;
}
[data-testid="stExpander"] > div > div {
    background: rgba(3,9,22,0.92) !important;
    border-top: 1px solid rgba(56,189,248,0.08) !important;
    border-radius: 0 0 9px 9px !important; padding: 10px !important;
}

/* ─── ALERTS ──────────────────────────────────  */
.stSuccess > div { background:rgba(34,197,94,0.08)!important; border:1px solid rgba(34,197,94,0.28)!important; border-radius:9px!important; color:#86efac!important; font-size:0.82rem!important; }
.stWarning > div { background:rgba(245,158,11,0.07)!important; border:1px solid rgba(245,158,11,0.25)!important; border-radius:9px!important; color:#fcd34d!important; font-size:0.82rem!important; }
.stError   > div { background:rgba(239,68,68,0.07)!important;  border:1px solid rgba(239,68,68,0.25)!important;  border-radius:9px!important; color:#fca5a5!important; font-size:0.82rem!important; }
.stInfo    > div { background:rgba(56,189,248,0.06)!important; border:1px solid rgba(56,189,248,0.2)!important;  border-radius:9px!important; color:#7dd3fc!important;  font-size:0.82rem!important; }

hr { border:none!important; border-top:1px solid rgba(56,189,248,0.09)!important; margin:10px 0!important; }
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
.security-line {
    text-align:center; color:#1e3a4a; font-size:0.68rem; letter-spacing:0.06em;
    margin-top:8px; display:flex; align-items:center; justify-content:center; gap:5px;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────
for k, v in {
    "resultado": None, "cotitular_activo": False,
    "cotitular_resultado": None, "ingreso": 0.0, "mensualidad": 0.0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── TOPBAR ─────────────────────────────────────────────────────────
tc1, tc2 = st.columns([1, 11])
with tc1:
    st.image("logo_new.png", width=72)
with tc2:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:16px;padding:6px 0;">
      <div>
        <div class="topbar-title">AutoScore AI</div>
        <div class="topbar-sub">Aprobación Inteligente</div>
      </div>
      <div class="topbar-divider"></div>
      <div style="color:#475569;font-size:0.72rem;letter-spacing:0.04em;">
        Herramienta de Pre-Análisis de Crédito Automotriz
      </div>
      <div class="topbar-badge" style="margin-left:auto;">🔒 Datos protegidos</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="height:1px;margin:0 0 14px;
background:linear-gradient(90deg,transparent,#38bdf8 25%,#8b5cf6 75%,transparent);
box-shadow:0 0 14px rgba(56,189,248,0.3);"></div>
""", unsafe_allow_html=True)

# ── DOS COLUMNAS ───────────────────────────────────────────────────
col_izq, col_der = st.columns([1, 1], gap="medium")

# ╔══════════════════════════════════╗
# ║      IZQUIERDA — FORMULARIO      ║
# ╚══════════════════════════════════╝
with col_izq:

    # ASESOR
    st.markdown('<div class="sec-label">👤 Datos del Asesor</div>', unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1: asesor = st.text_input("Nombre asesor", placeholder="Nombre completo")
    with a2: rfc    = st.text_input("RFC asesor", placeholder="XAXX010101000")
    b1, b2 = st.columns(2)
    with b1: telefono_asesor = st.text_input("Teléfono asesor", placeholder="55 1234 5678")
    with b2: correo_asesor   = st.text_input("Correo asesor", placeholder="asesor@correo.com")

    st.markdown("<div style='margin:4px 0'></div>", unsafe_allow_html=True)

    with st.form("formulario"):

        # CLIENTE
        st.markdown('<div class="sec-label">👥 Datos del Cliente</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: nombre_cliente = st.text_input("Nombre cliente", placeholder="Nombre completo")
        with c2: telefono       = st.text_input("Teléfono", placeholder="55 9876 5432")
        correo = st.text_input("Correo cliente", placeholder="cliente@correo.com")

        # PERFIL
        st.markdown('<div class="sec-label">📊 Perfil Financiero</div>', unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)
        with p1: edad   = st.number_input("Edad", 18, 73, 18)
        with p2: ingreso = st.number_input("Ingreso mensual ($)", min_value=6500.0, value=6500.0, step=500.0, format="%.0f")
        with p3: tipo_ingreso = st.selectbox("Tipo de ingreso", ["Nómina","Independiente","No comprueba"])

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

        st.markdown("<div style='margin:6px 0'></div>", unsafe_allow_html=True)
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

    if prob>=80:   sc="AZUL"
    elif prob>=70: sc="VERDE"
    elif prob>=45: sc="AMARILLO"
    elif prob>=35: sc="NARANJA"
    else:          sc="ROJO"

    msg_c=msg_a=""; decision="🟡 EN EVALUACIÓN"; plan="REVISION"
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

    # alertas
    alerta_cotitular   = "COTITULAR" in " ".join(condicionamientos)
    alerta_ingresos    = any(x in " ".join(condicionamientos) for x in ["INGRESO","INGRESOS","VALIDACIÓN"])
    alerta_investigacion = "INVESTIGACIÓN" in " ".join(condicionamientos) or "FÍSICA" in " ".join(condicionamientos)

    # investigación
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

    # semaforo css
    if "APROBADO" in decision and "FINANCIERA" not in decision: sem_class="verde"
    elif "FINANCIERA" in decision or "PRE" in decision:         sem_class="amarillo"
    elif "OPORTUNIDAD" in decision or "AJUSTE" in decision:     sem_class="naranja"
    else:                                                        sem_class="naranja"
    if "ALTERNATIVA" in decision: sem_class="rojo"

    # color probabilidad
    if prob>=70:   prob_col="#4ade80"
    elif prob>=50: prob_col="#facc15"
    elif prob>=35: prob_col="#fb923c"
    else:          prob_col="#f87171"

    # financiera sugerida
    if plan in ["AUTOMATICO","DIRECTO"]:       financiera="Automático"
    elif plan in ["SE VA A ANALISIS","CONDICIONADO"]: financiera="Condicionado"
    else:                                      financiera="Revisión especial"

    st.session_state.resultado = {
        "sc":sc, "prob":prob, "prob_col":prob_col,
        "temp":temp, "inv":inv, "decision":decision, "sem_class":sem_class,
        "plan":plan, "msg_c":msg_c, "msg_a":msg_a,
        "condicionamientos":condicionamientos,
        "alerta_cotitular":alerta_cotitular,
        "alerta_ingresos":alerta_ingresos,
        "alerta_investigacion":alerta_investigacion,
        "financiera":financiera,
        "enganche_pct":enganche_pct, "score":score, "perfil":perfil,
        "nombre":nombre_cliente, "telefono":telefono, "correo":correo,
        "asesor":asesor, "telefono_asesor":telefono_asesor,
        "correo_asesor":correo_asesor, "rfc":rfc,
        "docs":docs, "mensualidad":mensualidad, "cap_pago":cap_pago,
    }
    st.session_state.cotitular_activo    = (plan=="COTITULAR")
    st.session_state.cotitular_resultado = None

# ╔══════════════════════════════════╗
# ║    DERECHA — RESULTADO ANÁLISIS  ║
# ╚══════════════════════════════════╝
with col_der:

    if not st.session_state.resultado:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;
            justify-content:center;min-height:55vh;gap:12px;opacity:0.3;">
          <div style="font-size:3rem;">📊</div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:0.85rem;color:#38bdf8;
              text-transform:uppercase;letter-spacing:0.12em;text-align:center;">
              Resultado del Análisis<br>
              <span style="font-size:0.65rem;opacity:0.7;">Completa el formulario y presiona Analizar</span>
          </div>
        </div>""", unsafe_allow_html=True)

    else:
        r = st.session_state.resultado

        # ── ENCABEZADO RESULTADO ──────────────────────────────
        SCORE_MAP = {
            "AZUL":     ("🔵","SCORE AZUL",    "#38bdf8"),
            "VERDE":    ("🟢","SCORE VERDE",   "#22c55e"),
            "AMARILLO": ("🟡","SCORE AMARILLO","#eab308"),
            "NARANJA":  ("🟠","SCORE NARANJA", "#f97316"),
            "ROJO":     ("🔴","EN DESARROLLO", "#ef4444"),
        }
        em, lbl, col_hex = SCORE_MAP[r["sc"]]

        st.markdown(f"""
        <div class="res-header">
          <div class="res-title">Resultado de Análisis:</div>
          <div class="res-pct" style="color:{r['prob_col']};">{r['prob']}%</div>
        </div>
        """, unsafe_allow_html=True)

        # ── TABLA DE RESULTADOS (estilo Excel) ────────────────
        nivel_map = {"FUERTE":"Perfil fuerte","MEDIO":"Perfil medio","DELGADO":"Perfil delgado"}
        st.markdown(f"""
        <div class="row-table">
          <div class="row">
            <span class="lbl">Capacidad de pago estimada</span>
            <span class="val blue">$ {r['cap_pago']:,.2f}</span>
          </div>
          <div class="row">
            <span class="lbl">% de enganche</span>
            <span class="val {'green' if r['enganche_pct']>=20 else 'orange'}">{r['enganche_pct']:.0f}%</span>
          </div>
          <div class="row">
            <span class="lbl">Score perfil</span>
            <span class="val blue">{r['score']}</span>
          </div>
          <div class="row">
            <span class="lbl">Nivel perfil</span>
            <span class="val blue">{nivel_map.get(r['perfil'], r['perfil'])}</span>
          </div>
          <div class="row">
            <span class="lbl">Score crediticio</span>
            <span class="val" style="color:{col_hex};">{em} {lbl}</span>
          </div>
          <div class="row">
            <span class="lbl">Mensualidad estimada</span>
            <span class="val {'green' if r['mensualidad']<=r['cap_pago'] else 'red'}">$ {r['mensualidad']:,.0f}</span>
          </div>
          <div class="row">
            <span class="lbl">Financiera sugerida</span>
            <span class="val blue">{r['financiera']}</span>
          </div>
          <div class="row">
            <span class="lbl">Tipo de cliente</span>
            <span class="val {'green' if 'CALIENTE' in r['temp'] else ('yellow' if 'TIBIO' in r['temp'] else 'blue')}">{r['temp']}</span>
          </div>
          <div class="row">
            <span class="lbl">Sugerencia anticipo</span>
            <span class="val yellow">{'Enganche completo' if r['plan']=='DIRECTO' else 'Solicitar anticipo $5,000'}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── SEMÁFORO ──────────────────────────────────────────
        st.markdown(f"""
        <div class="semaforo {r['sem_class']}" style="margin-top:10px;">
            {'✅' if r['sem_class']=='verde' else ('⚠️' if r['sem_class']=='amarillo' else '🔴')}
            {r['decision']}
        </div>""", unsafe_allow_html=True)

        # ── ESTRATEGIA INTERNA ────────────────────────────────
        with st.expander("🔒 Estrategia interna — solo asesor"):
            st.markdown(f'<div class="estrategia-box">🔴 {r["msg_a"]}</div>', unsafe_allow_html=True)

        # ── RIESGOS / ALERTAS ─────────────────────────────────
        st.markdown('<div class="sec-label">⚠️ Riesgos detectados</div>', unsafe_allow_html=True)

        ac = "bad" if r["alerta_cotitular"]   else "ok"
        ai = "bad" if r["alerta_ingresos"]    else "ok"
        av = r["inv"]

        alerta_cotitular_txt  = "Requiere cotitular" if r["alerta_cotitular"] else "Sin alerta de cotitular"
        alerta_ingresos_txt   = "Validar ingresos"   if r["alerta_ingresos"]  else "Sin alerta de ingresos"

        st.markdown(f"""
        <div class="alerta-chip {ac}">
            {'🔴' if r['alerta_cotitular'] else '🟢'} ALERTA DE COTITULAR &nbsp;—&nbsp; {alerta_cotitular_txt}
        </div>
        <div class="alerta-chip {ai}">
            {'🔴' if r['alerta_ingresos'] else '🟢'} ALERTA DE INGRESOS &nbsp;—&nbsp; {alerta_ingresos_txt}
        </div>
        <div class="alerta-chip {'bad' if r['alerta_investigacion'] else 'ok'}">
            {'🔴' if r['alerta_investigacion'] else '🟢'} ALERTA DE INVESTIGACIÓN &nbsp;—&nbsp; {av}
        </div>
        """, unsafe_allow_html=True)

        # ── CONDICIONAMIENTOS ────────────────────────────────
        if r["condicionamientos"]:
            st.markdown('<div class="sec-label">📋 Tipos de condicionamientos</div>', unsafe_allow_html=True)
            cond_txt = ", ".join(r["condicionamientos"])
            st.markdown(f'<div class="cond-box">⚡ {cond_txt}</div>', unsafe_allow_html=True)

        # ── DOCUMENTACIÓN ─────────────────────────────────────
        st.markdown('<div class="sec-label">📄 Documentación requerida</div>', unsafe_allow_html=True)
        docs_html = " &nbsp;·&nbsp; ".join([f"📎 {d}" for d in r["docs"]])
        st.markdown(f'<div style="color:#94a3b8;font-size:0.78rem;padding:4px 0;">{docs_html}</div>', unsafe_allow_html=True)

        # ── CUENTA + COTIZADOR ───────────────────────────────
        st.markdown('<div class="sec-label">🏦 Cuenta para depósito</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="cuenta-box">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
              <div style="font-family:'Rajdhani',sans-serif;font-size:0.9rem;
                  font-weight:700;color:#e2e8f0;">DAOSA SA DE CV</div>
              <div style="color:#475569;font-size:0.78rem;margin-top:2px;">BBVA · 012320001250476847</div>
            </div>
            <div style="color:#38bdf8;font-size:0.65rem;letter-spacing:0.06em;
                text-transform:uppercase;font-weight:600;">Verificar antes<br>de transferir</div>
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
                cv1,cv2,cv3 = st.columns(3)
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
                style="margin-top:6px;font-size:0.82rem;">
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
                Paragraph(f"Estatus: {r['decision']}", sty["Normal"]),
                Paragraph(f"Probabilidad estimada: {r['prob']}%", sty["Normal"]),
                Paragraph(f"Mensualidad estimada: ${r.get('mensualidad',0):,.0f}", sty["Normal"]),
                Paragraph(f"Capacidad de pago: ${r.get('cap_pago',0):,.0f}", sty["Normal"]),
                Paragraph(f"Condicionamientos: {', '.join(r.get('condicionamientos',[]))}", sty["Normal"]),
                Paragraph(" ", sty["Normal"]),
                Paragraph("<b>Análisis:</b>", sty["Heading3"]),
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
