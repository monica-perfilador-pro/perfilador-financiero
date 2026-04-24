import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AutoScore AI", page_icon="🚗", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600&display=swap');

/* =========================
   FONDO TECNOLÓGICO
========================= */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: #060d1a !important;
    color: #e2e8f0;
    font-family: 'Exo 2', sans-serif;
}

/* GRID PATTERN OVERLAY */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(56,189,248,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,189,248,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    z-index: 0;
    pointer-events: none;
}

/* LUZ SUPERIOR */
[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    top: -300px;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
    height: 600px;
    background: radial-gradient(ellipse, rgba(56,189,248,0.12) 0%, rgba(139,92,246,0.06) 40%, transparent 70%);
    filter: blur(60px);
    z-index: 0;
    pointer-events: none;
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 1rem !important;
    padding-bottom: 2rem;
    max-width: 680px;
}

* { font-family: 'Exo 2', sans-serif; }

h1, h2, h3, h4 {
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 0.05em;
}

/* =========================
   CARD GLASS
========================= */
.card {
    background: linear-gradient(135deg, rgba(10,20,40,0.95) 0%, rgba(8,16,32,0.98) 100%);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 18px;
    padding: 28px 32px;
    backdrop-filter: blur(20px);
    box-shadow:
        0 0 0 1px rgba(56,189,248,0.05),
        0 20px 60px rgba(0,0,0,0.7),
        0 0 80px rgba(56,189,248,0.04),
        inset 0 1px 0 rgba(255,255,255,0.05);
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: "";
    position: absolute;
    top: -1px; left: -1px; right: -1px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.6), rgba(139,92,246,0.4), transparent);
    border-radius: 18px 18px 0 0;
}

.card::after {
    content: "";
    position: absolute;
    top: 0; right: 0;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(56,189,248,0.08), transparent 70%);
    pointer-events: none;
}

/* =========================
   SECTION HEADERS
========================= */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 22px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(56,189,248,0.15);
}

.section-header .icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, rgba(56,189,248,0.2), rgba(139,92,246,0.15));
    border: 1px solid rgba(56,189,248,0.3);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
}

.section-title {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.2rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0 !important;
}

/* =========================
   INPUTS
========================= */
.stTextInput input,
.stNumberInput input {
    background: rgba(4,12,28,0.9) !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: rgba(56,189,248,0.7) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.1), 0 0 20px rgba(56,189,248,0.15) !important;
    outline: none !important;
}

.stSelectbox > div > div {
    background: rgba(4,12,28,0.9) !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    border-radius: 10px !important;
    font-family: 'Exo 2', sans-serif !important;
}

label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #7dd3fc !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-family: 'Exo 2', sans-serif !important;
    margin-bottom: 4px !important;
}

/* =========================
   BOTÓN PRINCIPAL
========================= */
.stFormSubmitButton button,
.stButton button {
    width: 100% !important;
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 50%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 16px 32px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    box-shadow:
        0 0 30px rgba(99,102,241,0.4),
        0 0 60px rgba(56,189,248,0.15),
        inset 0 1px 0 rgba(255,255,255,0.2) !important;
    transition: all 0.3s ease !important;
    margin-top: 8px !important;
}

.stFormSubmitButton button:hover,
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow:
        0 0 40px rgba(99,102,241,0.6),
        0 0 80px rgba(56,189,248,0.25),
        inset 0 1px 0 rgba(255,255,255,0.3) !important;
}

hr {
    border: none !important;
    border-top: 1px solid rgba(56,189,248,0.12) !important;
    margin: 20px 0 !important;
}

/* =========================
   RESULTADOS
========================= */
.result-card {
    background: linear-gradient(135deg, rgba(10,20,40,0.97), rgba(6,14,28,0.99));
    border: 1px solid rgba(56,189,248,0.3);
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: "";
    position: absolute;
    top: -1px; left: -1px; right: -1px;
    height: 2px;
    background: linear-gradient(90deg, #38bdf8, #6366f1, #8b5cf6);
}

.prob-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.3);
    border-radius: 50px;
    padding: 6px 16px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #7dd3fc;
    letter-spacing: 0.05em;
    margin: 8px 0;
}

.mensaje-cliente {
    background: linear-gradient(135deg, rgba(56,189,248,0.06), rgba(99,102,241,0.04));
    border: 1px solid rgba(56,189,248,0.18);
    border-left: 3px solid #38bdf8;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    color: #cbd5e1;
    font-size: 0.9rem;
    margin: 12px 0;
    line-height: 1.6;
}

.doc-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    background: rgba(56,189,248,0.05);
    border: 1px solid rgba(56,189,248,0.1);
    border-radius: 8px;
    margin: 6px 0;
    color: #94a3b8;
    font-size: 0.88rem;
}

.security-badge {
    text-align: center;
    color: #475569;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.streamlit-expanderHeader {
    background: rgba(56,189,248,0.05) !important;
    border: 1px solid rgba(56,189,248,0.15) !important;
    border-radius: 10px !important;
    color: #7dd3fc !important;
    font-family: 'Exo 2', sans-serif !important;
}

.stCaption { color: #f59e0b !important; font-size: 0.78rem !important; }

.stNumberInput button {
    background: rgba(56,189,248,0.1) !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    color: #38bdf8 !important;
    border-radius: 6px !important;
    width: auto !important;
    padding: 4px 10px !important;
    margin: 0 !important;
    font-size: 1rem !important;
}

.stDownloadButton button {
    background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(99,102,241,0.12)) !important;
    border: 1px solid rgba(56,189,248,0.35) !important;
    color: #7dd3fc !important;
    border-radius: 10px !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    box-shadow: 0 0 20px rgba(56,189,248,0.1) !important;
    width: 100% !important;
    padding: 12px !important;
    margin-top: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO / LOGO
# =========================
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.image("logo_new.png", width=480)

st.markdown("""
<div style="
    width: 50%;
    height: 1px;
    margin: 0 auto 24px auto;
    background: linear-gradient(90deg, transparent, #38bdf8 40%, #8b5cf6 60%, transparent);
    box-shadow: 0 0 20px rgba(56,189,248,0.5);
"></div>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
for key, val in {
    "resultado": None,
    "cotitular_activo": False,
    "cotitular_resultado": None,
    "analizado": False,
    "ingreso": 0.0,
    "mensualidad": 0.0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# =========================
# ASESOR (fuera del form)
# =========================
st.markdown("""
<div class="card">
  <div class="section-header">
    <div class="icon">👤</div>
    <p class="section-title">Datos del Asesor</p>
  </div>
</div>
""", unsafe_allow_html=True)

asesor = st.text_input("Nombre asesor", placeholder="Escribe el nombre completo")
telefono_asesor = st.text_input("Teléfono asesor", placeholder="Ej. 55 1234 5678")
correo_asesor = st.text_input("Correo asesor", placeholder="ejemplo@correo.com")
rfc = st.text_input("RFC asesor", placeholder="Ej. XAXX010101000")

st.markdown('<div class="security-badge">🛡️ Tus datos están protegidos y seguros</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# =========================
# FORMULARIO PRINCIPAL
# =========================
with st.form("formulario"):

    # CLIENTE
    st.markdown("""
    <div class="card">
      <div class="section-header">
        <div class="icon">👥</div>
        <p class="section-title">Datos del Cliente</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
    nombre_cliente = st.text_input("Nombre cliente", placeholder="Nombre completo")
    telefono = st.text_input("Teléfono cliente", placeholder="Ej. 55 9876 5432")
    correo = st.text_input("Correo cliente", placeholder="cliente@correo.com")
    st.markdown("<br>", unsafe_allow_html=True)

    # PERFIL FINANCIERO
    st.markdown("""
    <div class="card">
      <div class="section-header">
        <div class="icon">📊</div>
        <p class="section-title">Perfil Financiero</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
    edad = st.number_input("Edad", 18, 73, 18)
    ingreso = st.number_input("Ingreso mensual ($)", min_value=6500.0, value=6500.0, step=500.0, format="%.2f")
    tipo_ingreso = st.selectbox("Tipo de ingreso", ["Nómina", "Independiente", "No comprueba ingresos"])
    negocio_casa = st.selectbox("¿Negocio en domicilio?", [1, 2], format_func=lambda x: "Sí" if x == 1 else "No")
    if tipo_ingreso == "Independiente":
        st.caption("⚠️ Solo aplica para independientes")
    domicilio = st.selectbox("Antigüedad domicilio", [1,2,3],
        format_func=lambda x: ["Menos de 1 año","1 a 3 años","Más de 3 años"][x-1])
    domicilio_buro = st.selectbox("¿Domicilio coincide con identificaciones?", [1,2],
        format_func=lambda x: "Sí" if x==1 else "No")
    st.markdown("<br>", unsafe_allow_html=True)

    # VEHÍCULO
    st.markdown("""
    <div class="card">
      <div class="section-header">
        <div class="icon">🚗</div>
        <p class="section-title">Datos del Vehículo</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
    precio = st.number_input("Precio del vehículo ($)", min_value=0.0, format="%0.2f")
    enganche = st.number_input("Enganche ($)", min_value=0.0, format="%0.2f")
    plazo = st.selectbox("Plazo (meses)", [12, 24, 36, 48, 60, 72])
    consultas = st.number_input("Consultas / créditos recientes (últimos 3 meses)", 0, 20)
    st.markdown("<br>", unsafe_allow_html=True)

    # HISTORIAL CREDITICIO
    st.markdown("""
    <div class="card">
      <div class="section-header">
        <div class="icon">🏦</div>
        <p class="section-title">Historial Crediticio</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
    auto = st.selectbox("Crédito automotriz previo", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    credinissan = st.selectbox("CrediNissan", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    hipotecario = st.selectbox("Hipotecario", [1,2,3],
        format_func=lambda x: ["Bancario","Infonavit","No tiene"][x-1])
    tarjeta_alta = st.selectbox("Tarjetas mayores a $100K", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    tarjeta_baja = st.selectbox("Tarjetas menores a $100K o departamentales", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    atrasos = st.selectbox("Atrasos en buró", [1,2,3],
        format_func=lambda x: ["1-30 días","31-60 días","Más de 61 días"][x-1])
    st.markdown("<br>", unsafe_allow_html=True)

    # PERFIL DE COMPRA
    st.markdown("""
    <div class="card">
      <div class="section-header">
        <div class="icon">🔥</div>
        <p class="section-title">Perfil de Compra</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
    enganche_disp = st.selectbox("¿Tiene enganche disponible?", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    compra_mes = st.selectbox("¿Compra este mes?", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    unidad = st.selectbox("¿Hay unidad disponible?", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    st.markdown("<br>", unsafe_allow_html=True)

    submitted = st.form_submit_button("✦  ANALIZAR PERFIL FINANCIERO")

# =========================
# LÓGICA DE ANÁLISIS
# =========================
if submitted:
    st.session_state.analizado = True
    st.session_state.ingreso = ingreso

    monto = max(precio - enganche, 0)
    tasa_mensual = 0.015
    if plazo > 0 and monto > 0:
        mensualidad = monto * (tasa_mensual * (1 + tasa_mensual) ** plazo) / ((1 + tasa_mensual) ** plazo - 1)
    else:
        mensualidad = 0
    st.session_state.mensualidad = mensualidad

    enganche_pct = (enganche / precio) * 100 if precio > 0 else 0

    riesgo_alto = False
    riesgo_medio = False
    if atrasos == 3:                            riesgo_alto = True
    if consultas >= 8:                          riesgo_alto = True
    elif consultas >= 5:                        riesgo_medio = True
    if tipo_ingreso == "Independiente":         riesgo_medio = True
    if tipo_ingreso == "No comprueba ingresos": riesgo_alto = True
    if enganche_pct < 10:                       riesgo_alto = True
    elif enganche_pct < 20:                     riesgo_medio = True

    score = 0
    if tarjeta_alta == 1:                       score += 4
    if tarjeta_baja == 1 and ingreso > 30000:   score += 1
    if credinissan == 1:                        score += 5
    if auto == 1:                               score += 3
    if hipotecario == 1:                        score += 3
    elif hipotecario == 2:                      score += 1
    if atrasos == 2:                            score -= 3
    elif atrasos == 3:                          score -= 10
    if consultas >= 8:                          score -= 12
    elif consultas >= 5:                        score -= 6
    elif consultas >= 3:                        score -= 3

    perfil = "DELGADO" if score <= 0 else ("FUERTE" if score >= 7 else "MEDIO")
    prob = 85 if perfil == "FUERTE" else (65 if perfil == "MEDIO" else 30)
    if enganche_pct >= 40:   prob += 10
    elif enganche_pct >= 25: prob += 5
    if consultas >= 8:       prob -= 25
    elif consultas >= 5:     prob -= 15
    elif consultas >= 3:     prob -= 5
    prob = max(5, min(95, prob))

    if tipo_ingreso == "Nómina": capacidad_pago = ingreso / 2
    else:                        capacidad_pago = ingreso / 3.33
    excede_capacidad = mensualidad > capacidad_pago

    if compra_mes == 2:                                             temp = "❄️ FRÍO"
    elif compra_mes == 1 and enganche_disp == 1 and unidad == 1:   temp = "🔥 CALIENTE"
    else:                                                           temp = "🟡 TIBIO"

    if prob >= 80:   score_color = "AZUL"
    elif prob >= 70: score_color = "VERDE"
    elif prob >= 45: score_color = "AMARILLO"
    elif prob >= 35: score_color = "NARANJA"
    else:            score_color = "ROJO"

    mensaje_cliente = ""
    mensaje_asesor = ""
    decision = "🟡 EN EVALUACIÓN"
    plan = "REVISION"

    if consultas >= 10:
        decision = "🟠 ESTRATEGIA ALTERNATIVA"; plan = "COTITULAR"
    elif riesgo_alto and perfil != "FUERTE":
        decision = "🟠 ESTRATEGIA ALTERNATIVA"; plan = "ALTERNATIVA"
        mensaje_cliente = "Tu perfil puede avanzar mediante una alternativa de financiamiento."
        mensaje_asesor = "Riesgo alto detectado: subir enganche mínimo al 10% / comprobar ingresos / buscar cotitular."
    elif atrasos == 3:
        decision = "🟠 ESTRATEGIA ALTERNATIVA"; plan = "ALTERNATIVA"
        mensaje_cliente = "Tu perfil puede avanzar mediante una alternativa de financiamiento."
        mensaje_asesor = "Subir enganche / cotitular / evitar consultas."
    elif score_color == "ROJO":
        decision = "🟠 ESTRATEGIA ALTERNATIVA"; plan = "COTITULAR"
        mensaje_cliente = "Tu perfil actualmente requiere una alternativa de financiamiento."
        mensaje_asesor = "Buscar cotitular fuerte / Subir enganche / Evitar más consultas en buró."
    elif excede_capacidad and prob < 70:
        decision = "🟡 AJUSTE NECESARIO"; plan = "AJUSTAR_PLAZO"
        mensaje_cliente = "La mensualidad puede ajustarse para mejorar tu perfil."
        mensaje_asesor = "Ampliar plazo / Reducir monto a financiar / Validar ingresos."
    elif riesgo_medio and prob < 60:
        decision = "🟠 PERFIL CON OPORTUNIDAD"; plan = "RESCATE"
        mensaje_cliente = "Tu perfil tiene alta posibilidad de avanzar ajustando algunos puntos clave."
        mensaje_asesor = "Subir enganche (ideal 25%+) / Buscar cotitular línea directa / Evitar más consultas en buró."
    elif prob >= 70:
        if riesgo_medio:
            decision = "🟢 APROBADO EN ANÁLISIS DE FINANCIERA"; plan = "SE VA A ANALISIS"
            mensaje_cliente = "Tu perfil es viable y puede avanzar a proceso de aprobación, con validaciones normales."
            mensaje_asesor = "Posible validación de ingresos / Investigación telefónica."
        else:
            decision = "🟢 APROBADO"; plan = "AUTOMATICO"
            mensaje_cliente = "Tu perfil cumple con los criterios para avanzar en automático."
            mensaje_asesor = "Perfil limpio. Proceder directo."
    elif prob >= 50:
        if enganche_pct < 20 or riesgo_medio:
            decision = "🟡 APROBABLE CON AJUSTES"; plan = "CONDICIONADO"
            mensaje_cliente = "Tu perfil es viable realizando algunos ajustes."
            mensaje_asesor = "Subir enganche (+15 pts ideal) / Validación por financiera."
        else:
            decision = "🟡 PRE APROBADO"; plan = "DIRECTO"
            mensaje_cliente = "Tu perfil es favorable para avanzar."
            mensaje_asesor = "Perfil estable. Proceder."
    elif prob >= 35:
        decision = "🟡 PERFIL MEJORABLE"; plan = "COTITULAR"
        mensaje_cliente = "Tu perfil puede fortalecerse con apoyo adicional."
        mensaje_asesor = "Integrar cotitular fuerte / Comprobar ingresos / Mejorar enganche."
    else:
        decision = "🟠 ESTRATEGIA ALTERNATIVA"; plan = "ALTERNATIVA"
        mensaje_cliente = "Tu perfil puede avanzar mediante una alternativa de financiamiento."
        mensaje_asesor = "Financiera flexible / Reestructura de perfil."

    investigacion = "🟢 Sin validaciones relevantes"
    if tipo_ingreso != "Nómina" and prob < 45:
        investigacion = "🔴 Validación adicional requerida"
    if domicilio_buro == 2:
        investigacion = "🔴 Validación de domicilio"
    if tipo_ingreso == "Independiente":
        investigacion = "🟡 Validación de ingresos"
    if tipo_ingreso == "Independiente" and negocio_casa == 1:
        prob = max(prob, 80)
        investigacion = "🔴 Requiere validación física"

    documentos = ["INE", "Comprobante de domicilio"]
    if plan == "DIRECTO":       documentos = ["INE", "Comprobante", "Cotización"]
    elif plan == "COTITULAR":   documentos += ["Cotitular obligatorio"]
    elif tipo_ingreso == "Nómina": documentos += ["Nómina", "Estado de cuenta"]
    else:                       documentos += ["Estados de cuenta"]

    st.session_state.resultado = {
        "perfil": perfil, "score_color": score_color, "prob": prob,
        "temp": temp, "investigacion": investigacion, "decision": decision,
        "plan": plan, "mensaje_cliente": mensaje_cliente, "mensaje_asesor": mensaje_asesor,
        "nombre": nombre_cliente, "telefono": telefono, "correo": correo,
        "asesor": asesor, "telefono_asesor": telefono_asesor,
        "correo_asesor": correo_asesor, "rfc": rfc,
        "documentos": documentos, "mensualidad": mensualidad, "capacidad_pago": capacidad_pago,
    }
    st.session_state.cotitular_activo = (plan == "COTITULAR")
    st.session_state.cotitular_resultado = None

# =========================
# RESULTADO
# =========================
if st.session_state.resultado:
    r = st.session_state.resultado

    score_map = {
        "AZUL":     ("🔵", "SCORE AZUL",     "#38bdf8", "Perfil fuerte — alta probabilidad de aprobación"),
        "VERDE":    ("🟢", "SCORE VERDE",    "#22c55e", "Buen perfil — aprobado con condiciones normales"),
        "AMARILLO": ("🟡", "SCORE AMARILLO", "#eab308", "Perfil medio — requiere validación adicional"),
        "NARANJA":  ("🟠", "SCORE NARANJA",  "#f97316", "Perfil débil — requiere cotitular o mayor enganche"),
        "ROJO":     ("🟠", "EN DESARROLLO",  "#ef4444", "Perfil con oportunidad mediante estrategia alternativa"),
    }
    emoji, label, color, desc = score_map[r["score_color"]]

    st.markdown(f"""
    <div class="result-card">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
            <span style="font-size:1.8rem;">{emoji}</span>
            <div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:1.4rem; font-weight:700;
                    color:{color}; letter-spacing:0.08em;">{label}</div>
                <div style="color:#94a3b8; font-size:0.85rem;">{desc}</div>
            </div>
        </div>
        <div class="prob-badge">⚡ Probabilidad de aprobación: {r['prob']}%</div>
        <div style="display:flex; gap:16px; margin-top:14px; flex-wrap:wrap;">
            <div style="background:rgba(56,189,248,0.07); border:1px solid rgba(56,189,248,0.18);
                border-radius:10px; padding:10px 18px; flex:1; min-width:140px;">
                <div style="color:#7dd3fc; font-size:0.7rem; text-transform:uppercase;
                    letter-spacing:0.06em; margin-bottom:4px;">Capacidad de pago</div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:1.3rem;
                    font-weight:700; color:#e2e8f0;">${r['capacidad_pago']:,.0f}</div>
            </div>
            <div style="background:rgba(99,102,241,0.07); border:1px solid rgba(99,102,241,0.18);
                border-radius:10px; padding:10px 18px; flex:1; min-width:140px;">
                <div style="color:#a5b4fc; font-size:0.7rem; text-transform:uppercase;
                    letter-spacing:0.06em; margin-bottom:4px;">Mensualidad estimada</div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:1.3rem;
                    font-weight:700; color:#e2e8f0;">${r['mensualidad']:,.0f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "APROBADO" in r["decision"]:         st.success(r["decision"])
    elif "ALTERNATIVA" in r["decision"] or "OPORTUNIDAD" in r["decision"]: st.warning(r["decision"])
    elif "AJUSTE" in r["decision"]:         st.warning(r["decision"])
    else:                                   st.info(r["decision"])

    if r.get("mensaje_cliente"):
        st.markdown(f'<div class="mensaje-cliente">💡 {r["mensaje_cliente"]}</div>', unsafe_allow_html=True)

    with st.expander("🔒 Estrategia interna — solo asesor"):
        st.markdown(f"""
        <div style="background:rgba(239,68,68,0.05); border:1px solid rgba(239,68,68,0.15);
            border-radius:10px; padding:14px; color:#fca5a5; font-size:0.88rem;">
            {r.get("mensaje_asesor", "")}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="font-family:Rajdhani,sans-serif; font-size:1rem; font-weight:700; color:#7dd3fc; text-transform:uppercase; letter-spacing:0.08em; margin:18px 0 10px 0;">🔎 Validaciones requeridas</div>', unsafe_allow_html=True)
    st.write(r["investigacion"])

    st.markdown('<div style="font-family:Rajdhani,sans-serif; font-size:1rem; font-weight:700; color:#7dd3fc; text-transform:uppercase; letter-spacing:0.08em; margin:18px 0 10px 0;">📄 Documentación necesaria</div>', unsafe_allow_html=True)
    for d in r["documentos"]:
        st.markdown(f'<div class="doc-item">📎 {d}</div>', unsafe_allow_html=True)

    # COTITULAR
    if st.session_state.cotitular_activo:
        st.markdown("""
        <div style="font-family:Rajdhani,sans-serif; font-size:1.1rem; font-weight:700;
            color:#f59e0b; text-transform:uppercase; letter-spacing:0.08em;
            margin:24px 0 12px 0; padding:12px 16px;
            background:rgba(245,158,11,0.07); border:1px solid rgba(245,158,11,0.2);
            border-radius:10px;">
            👥 Análisis de Cotitular Requerido
        </div>
        """, unsafe_allow_html=True)
        with st.form("formulario_cotitular"):
            tipo_cot = st.selectbox("Tipo cotitular", ["Línea directa", "Conocido"])
            ingreso_cot = st.number_input("Ingreso cotitular ($)", min_value=0.0, step=500.0)
            auto_cot = st.selectbox("Automotriz cotitular", ["Sí", "No"])
            credinissan_cot = st.selectbox("CrediNissan cotitular", ["Sí", "No"])
            hipotecario_cot = st.selectbox("Hipotecario cotitular", ["No tiene", "Infonavit", "Bancario"])
            tarjeta_alta_cot = st.selectbox("Tarjetas >$100K cotitular", ["Sí", "No"])
            atrasos_cot = st.selectbox("Buró cotitular", ["Sin atrasos", "1-30 días", "31-60 días", "61+ días"])
            submit_cot = st.form_submit_button("✦  EVALUAR COTITULAR")

        if submit_cot:
            score_cot = 0
            if auto_cot == "Sí":                 score_cot += 3
            if credinissan_cot == "Sí":          score_cot += 5
            if hipotecario_cot == "Bancario":    score_cot += 4
            elif hipotecario_cot == "Infonavit": score_cot += 2
            if tarjeta_alta_cot == "Sí":         score_cot += 4
            if atrasos_cot == "Sin atrasos":     score_cot += 5
            elif atrasos_cot == "1-30 días":     score_cot += 2
            elif atrasos_cot == "31-60 días":    score_cot -= 4
            elif atrasos_cot == "61+ días":      score_cot -= 10

            capacidad_total = (st.session_state.ingreso + ingreso_cot) * 0.3
            mensualidad_guardada = st.session_state.mensualidad
            buro_cot = "BUENO" if score_cot >= 12 else ("REGULAR" if score_cot >= 6 else "MALO")

            if tipo_cot == "Conocido" and buro_cot != "BUENO":
                resultado_cot = "❌ Debe ser línea directa con buen historial"
            elif capacidad_total >= mensualidad_guardada and buro_cot == "BUENO":
                resultado_cot = "🟢 APROBADO FINAL"
            elif buro_cot == "REGULAR":
                resultado_cot = "🟡 Aún condicionado — mejorar perfil"
            else:
                resultado_cot = "🔴 Cotitular no viable"

            st.session_state.cotitular_resultado = resultado_cot

    if st.session_state.cotitular_resultado:
        st.markdown(f"""
        <div class="result-card" style="margin-top:12px;">
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:700;
                color:#e2e8f0; letter-spacing:0.06em;">RESULTADO FINAL COTITULAR</div>
            <div style="margin-top:8px; font-size:1rem;">{st.session_state.cotitular_resultado}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    st.markdown('<div style="font-family:Rajdhani,sans-serif; font-size:1rem; font-weight:700; color:#7dd3fc; text-transform:uppercase; letter-spacing:0.08em; margin:10px 0;">🔥 Temperatura de venta</div>', unsafe_allow_html=True)
    if "CALIENTE" in r["temp"]:  st.success(r["temp"])
    elif "TIBIO" in r["temp"]:   st.warning(r["temp"])
    else:                        st.info(r["temp"])

    st.markdown('<div style="font-family:Rajdhani,sans-serif; font-size:1rem; font-weight:700; color:#7dd3fc; text-transform:uppercase; letter-spacing:0.08em; margin:18px 0 10px 0;">💰 Siguiente paso</div>', unsafe_allow_html=True)
    if r["plan"] == "DIRECTO": st.success("👉 Solicitar ENGANCHE COMPLETO")
    else:                      st.warning("👉 Solicitar APARTADO $5,000")
    st.error("⚠️ Solicita anticipo para asegurar unidad")

    st.markdown("""
    <div class="result-card" style="margin-top:16px;">
        <div style="font-family:'Rajdhani',sans-serif; font-size:0.85rem; font-weight:700;
            color:#7dd3fc; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
            🏦 Cuenta para depósito — BBVA
        </div>
        <div style="font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:600; color:#e2e8f0; letter-spacing:0.04em;">DAOSA SA DE CV</div>
        <div style="color:#94a3b8; font-size:0.88rem; margin-top:4px;">012320001250476847</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("📊 Abrir Cotizador", "https://procotiza.losnrtelepro.com.mx/Procotiza/login.aspx?mns", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # PDF
    datos_completos = all([r.get("asesor","").strip(), r.get("nombre","").strip(), r.get("telefono","").strip()])
    if not datos_completos:
        st.warning("⚠️ Completa datos de cliente y asesor para generar PDF")
    else:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        content = [
            Paragraph("SOLICITUD DE PERFILAMIENTO CREDITICIO", styles["Title"]),
            Paragraph(" ", styles["Normal"]),
            Paragraph(f"<b>Cliente:</b> {r.get('nombre','')}", styles["Normal"]),
            Paragraph(f"<b>Teléfono:</b> {r.get('telefono','')}", styles["Normal"]),
            Paragraph(f"<b>Correo:</b> {r.get('correo','')}", styles["Normal"]),
            Paragraph(" ", styles["Normal"]),
            Paragraph("<b>RESULTADO DE PERFIL</b>", styles["Heading2"]),
            Paragraph(f"Estatus: {r['decision']}", styles["Normal"]),
            Paragraph(f"Probabilidad estimada: {r['prob']}%", styles["Normal"]),
            Paragraph(f"<b>Mensualidad estimada:</b> ${r.get('mensualidad',0):,.0f}", styles["Normal"]),
            Paragraph(f"<b>Capacidad de pago máxima:</b> ${r.get('capacidad_pago',0):,.0f}", styles["Normal"]),
            Paragraph("<b>Resultado del análisis:</b>", styles["Heading3"]),
            Paragraph(r.get("mensaje_cliente",""), styles["Normal"]),
            Paragraph(" ", styles["Normal"]),
            Paragraph("<b>Posibles validaciones durante el proceso:</b>", styles["Heading3"]),
            Paragraph("- Validación de ingresos\n- Confirmación de datos\n- Revisión por financiera", styles["Normal"]),
            Paragraph(" ", styles["Normal"]),
            Paragraph("<b>ASEGURA TU UNIDAD</b>", styles["Heading2"]),
            Paragraph("Puedes iniciar tu trámite mediante apartado.", styles["Normal"]),
            Paragraph(" ", styles["Normal"]),
            Paragraph("<b>Cuentas para depósito:</b>", styles["Normal"]),
            Paragraph("Banco Principal BBVA: 012320001250476847", styles["Normal"]),
            Paragraph(" ", styles["Normal"]),
            Paragraph("Importante:", styles["Heading3"]),
            Paragraph("• Cuenta nombre de DAOSA SA DE CV (verifica antes de transferir)", styles["Normal"]),
            Paragraph("• El concepto debe incluir el nombre del titular del crédito", styles["Normal"]),
            Paragraph("• Favor de enviar comprobante de pago a tu asesor", styles["Normal"]),
            Paragraph(" ", styles["Normal"]),
            Paragraph("<b>Contacto</b>", styles["Heading2"]),
            Paragraph(f"<b>Asesor:</b> {r.get('asesor','')}", styles["Normal"]),
            Paragraph(f"<b>Teléfono:</b> {r.get('telefono_asesor','')}", styles["Normal"]),
            Paragraph(f"<b>Correo:</b> {r.get('correo_asesor','')}", styles["Normal"]),
            Paragraph(f"<b>RFC:</b> {r.get('rfc','')}", styles["Normal"]),
            Paragraph(" ", styles["Normal"]),
            Paragraph("Tu asesor está disponible para acompañarte en todo el proceso.", styles["Normal"]),
            Paragraph(" ", styles["Normal"]),
            Paragraph("<b>Nota importante:</b>", styles["Heading3"]),
            Paragraph("Este documento es informativo. La aprobación final dependerá de la evaluación de la financiera conforme a buró de crédito.", styles["Normal"]),
        ]
        doc.build(content)
        st.download_button(
            "📄 Descargar PDF del perfil",
            data=buffer.getvalue(),
            file_name="perfil_autoscore.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.markdown('<div class="security-badge" style="margin-top:20px;">🛡️ Tus datos están protegidos y seguros</div>', unsafe_allow_html=True)
