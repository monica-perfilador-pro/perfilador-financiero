import streamlit as st
import datetime

st.set_page_config(page_title="AutoScore AI — Dashboard F&I", page_icon="📊", layout="wide")

SHEET_ID   = "1f0oXowVTkuZdtlzw3Cdx5IIJRc9XIU6n0zM-EaXlyAA"
SHEET_NAME = "AutoScore Perfiles"
PASSWORD   = "autoscore2024"

# ── PALETA ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Exo+2:wght@400;500;600&display=swap');
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"] {
    background: #f8f8f8 !important; color: #111 !important;
    font-family: 'Exo 2', sans-serif !important;
}
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }
/* Header */
.dash-header {
    background: #111; padding: 14px 24px; margin: -1.5rem -2rem 1.5rem;
    display: flex; align-items: center; gap: 16px;
}
.dash-title { font-family:'Rajdhani',sans-serif; font-size:1.4rem;
    font-weight:700; color:#fff; letter-spacing:0.08em; }
.dash-sub { font-size:0.65rem; color:#c3002f; letter-spacing:0.16em;
    text-transform:uppercase; margin-top:2px; }
.red-line { height:2px; background:#c3002f; margin: 0 -2rem 1.5rem; }
/* Métricas */
.metric-row { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:20px; }
.metric-card { background:#fff; border:0.5px solid #e0e0e0; border-radius:10px;
    padding:14px 16px; border-top:3px solid #c3002f; }
.metric-label { font-size:0.65rem; color:#888; text-transform:uppercase;
    letter-spacing:0.08em; margin-bottom:4px; }
.metric-value { font-family:'Rajdhani',sans-serif; font-size:1.8rem;
    font-weight:700; color:#111; line-height:1; }
.metric-sub { font-size:0.7rem; color:#aaa; margin-top:3px; }
/* Badges score */
.badge { display:inline-block; padding:3px 10px; border-radius:50px;
    font-size:0.72rem; font-weight:600; letter-spacing:0.04em; }
.badge-AZUL     { background:#eff8ff; color:#0369a1; }
.badge-VERDE    { background:#f0fdf4; color:#166534; }
.badge-AMARILLO { background:#fefce8; color:#854d0e; }
.badge-NARANJA  { background:#fff7ed; color:#9a3412; }
.badge-ROJO     { background:#fff5f5; color:#9f1239; }
/* Tabla */
.stDataFrame { border-radius:10px !important; }
/* Login */
.login-box { max-width:360px; margin:80px auto; background:#fff;
    border:0.5px solid #e0e0e0; border-radius:16px; padding:36px;
    border-top:3px solid #c3002f; }
/* Inputs */
.stTextInput input { border:1px solid #ddd !important; border-radius:8px !important;
    font-size:0.88rem !important; }
.stTextInput input:focus { border-color:#c3002f !important; box-shadow:0 0 0 2px rgba(195,0,47,0.1) !important; }
label,[data-testid="stWidgetLabel"] p {
    color:#c3002f !important; font-size:0.68rem !important;
    font-weight:600 !important; letter-spacing:0.08em !important;
    text-transform:uppercase !important; }
.stButton>button { background:#c3002f !important; color:#fff !important;
    border:none !important; border-radius:50px !important; padding:10px 24px !important;
    font-family:'Rajdhani',sans-serif !important; font-weight:700 !important;
    font-size:0.9rem !important; letter-spacing:0.1em !important;
    width:100% !important; box-shadow:0 2px 12px rgba(195,0,47,0.3) !important; }
.stSelectbox>div>div { border:1px solid #ddd !important; border-radius:8px !important; }
hr { border:none !important; border-top:1px solid #e5e5e5 !important; margin:16px 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── LOGIN ─────────────────────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("""
    <div style="height:2px;background:#c3002f;margin:-1.5rem -2rem 0;"></div>
    <div class="login-box">
      <div style="text-align:center;margin-bottom:24px;">
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.6rem;
            font-weight:700;color:#111;">AutoScore <span style="color:#c3002f;">AI</span></div>
        <div style="font-size:0.65rem;color:#c3002f;letter-spacing:0.16em;
            text-transform:uppercase;margin-top:4px;">Dashboard F&amp;I</div>
        <div style="font-size:0.75rem;color:#888;margin-top:8px;">
            Solo para uso interno — Gerencia y F&amp;I</div>
      </div>
    """, unsafe_allow_html=True)

    pwd = st.text_input("Contraseña de acceso", type="password", placeholder="••••••••••")
    if st.button("INGRESAR"):
        if pwd == PASSWORD:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ── CARGAR DATOS ──────────────────────────────────────────────────
@st.cache_data(ttl=60)
def cargar_datos():
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly"
        ]
        creds = Credentials.from_service_account_info(
            dict(st.secrets["gcp_service_account"]), scopes=scopes)
        service = build("sheets", "v4", credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            range=f"{SHEET_NAME}!A1:R1000"
        ).execute()

        valores = result.get("values", [])
        if len(valores) < 2:
            return []

        headers = valores[0]
        filas   = []
        for row in valores[1:]:
            while len(row) < len(headers):
                row.append("")
            filas.append(dict(zip(headers, row)))
        return filas

    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return []


# ── HEADER ────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div>
    <div class="dash-title">AutoScore AI — Dashboard</div>
    <div class="dash-sub">Panel F&amp;I · Solo uso interno</div>
  </div>
</div>
<div class="red-line"></div>
""", unsafe_allow_html=True)

# ── CARGAR Y VALIDAR ──────────────────────────────────────────────
datos = cargar_datos()

if not datos:
    st.markdown("""
    <div style="text-align:center;padding:60px 0;color:#aaa;">
      <div style="font-size:2.5rem;margin-bottom:12px;">📋</div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;
          text-transform:uppercase;letter-spacing:0.1em;">
          Sin perfiles aún
      </div>
      <div style="font-size:0.78rem;margin-top:8px;">
          Los análisis aparecerán aquí automáticamente
      </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Actualizar"):
        st.cache_data.clear()
        st.rerun()
    st.stop()

# ── FILTROS ───────────────────────────────────────────────────────
f1, f2, f3, f4 = st.columns([2, 2, 2, 1])

asesores = ["Todos"] + sorted(set(d.get("Asesor","") for d in datos if d.get("Asesor","")))
scores   = ["Todos", "AZUL", "VERDE", "AMARILLO", "NARANJA", "ROJO"]

with f1:
    filtro_asesor = st.selectbox("Asesor", asesores)
with f2:
    filtro_score  = st.selectbox("Score", scores)
with f3:
    filtro_fecha  = st.text_input("Buscar cliente o fecha", placeholder="Ej: Juan / 26/04/2026")
with f4:
    st.markdown("<div style='margin-top:22px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Actualizar"):
        st.cache_data.clear()
        st.rerun()

# Aplicar filtros
filtrados = datos
if filtro_asesor != "Todos":
    filtrados = [d for d in filtrados if d.get("Asesor","") == filtro_asesor]
if filtro_score != "Todos":
    filtrados = [d for d in filtrados if d.get("Score","") == filtro_score]
if filtro_fecha:
    q = filtro_fecha.lower()
    filtrados = [d for d in filtrados
                 if q in d.get("Cliente","").lower()
                 or q in d.get("Fecha","").lower()]

# ── MÉTRICAS RESUMEN ──────────────────────────────────────────────
total    = len(filtrados)
aprobados= sum(1 for d in filtrados if "APROBADO" in d.get("Decision",""))
sc_dist  = {}
for d in filtrados:
    sc = d.get("Score","")
    sc_dist[sc] = sc_dist.get(sc, 0) + 1

prob_vals = []
for d in filtrados:
    try: prob_vals.append(float(d.get("Probabilidad",0)))
    except: pass
avg_prob = round(sum(prob_vals)/len(prob_vals)) if prob_vals else 0

pct_aprob = round(aprobados/total*100) if total > 0 else 0

st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="metric-label">Total perfiles</div>
    <div class="metric-value">{total}</div>
    <div class="metric-sub">analizados</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Aprobados</div>
    <div class="metric-value" style="color:#166534;">{aprobados}</div>
    <div class="metric-sub">{pct_aprob}% del total</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Prob. promedio</div>
    <div class="metric-value">{avg_prob}%</div>
    <div class="metric-sub">de aprobación</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Score azul/verde</div>
    <div class="metric-value" style="color:#0369a1;">
        {sc_dist.get('AZUL',0) + sc_dist.get('VERDE',0)}
    </div>
    <div class="metric-sub">perfiles fuertes</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Requieren acción</div>
    <div class="metric-value" style="color:#c3002f;">
        {sc_dist.get('NARANJA',0) + sc_dist.get('ROJO',0)}
    </div>
    <div class="metric-sub">naranja + rojo</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── TABLA DE PERFILES ─────────────────────────────────────────────
st.markdown(f"""
<div style="font-family:'Rajdhani',sans-serif;font-size:0.8rem;font-weight:700;
    color:#c3002f;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;">
    📋 Perfiles analizados — {total} registros
</div>
""", unsafe_allow_html=True)

import pandas as pd

if filtrados:
    # Construir tabla limpia
    filas_tabla = []
    for d in reversed(filtrados):  # más recientes primero
        sc = d.get("Score","")
        badge = f'<span class="badge badge-{sc}">{sc}</span>' if sc else ""
        filas_tabla.append({
            "Fecha":      d.get("Fecha",""),
            "Hora":       d.get("Hora",""),
            "Asesor":     d.get("Asesor",""),
            "Cliente":    d.get("Cliente",""),
            "Teléfono":   d.get("Tel_Cliente",""),
            "Score":      d.get("Score",""),
            "Prob %":     d.get("Probabilidad",""),
            "Decisión":   d.get("Decision",""),
            "Cap. Pago":  f'${float(d.get("Capacidad_Pago",0) or 0):,.0f}',
            "Mensualidad":f'${float(d.get("Mensualidad",0) or 0):,.0f}',
            "Temperatura":d.get("Temp",""),
            "Condiciones":d.get("Condicionamientos",""),
        })

    df = pd.DataFrame(filas_tabla)

    # Colorear score en la tabla
    def color_score(val):
        colores = {
            "AZUL":     "background-color:#eff8ff;color:#0369a1;font-weight:600",
            "VERDE":    "background-color:#f0fdf4;color:#166534;font-weight:600",
            "AMARILLO": "background-color:#fefce8;color:#854d0e;font-weight:600",
            "NARANJA":  "background-color:#fff7ed;color:#9a3412;font-weight:600",
            "ROJO":     "background-color:#fff5f5;color:#9f1239;font-weight:600",
        }
        return colores.get(val, "")

    styled = df.style.applymap(color_score, subset=["Score"])
    st.dataframe(styled, use_container_width=True, height=480)

    # ── DESCARGAR EXCEL ───────────────────────────────────────────
    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
    buf_excel = pd.ExcelWriter.__new__(pd.ExcelWriter)
    from io import BytesIO
    buf_xl = BytesIO()
    with pd.ExcelWriter(buf_xl, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Perfiles AutoScore")
    st.download_button(
        "📥 Descargar tabla en Excel",
        data=buf_xl.getvalue(),
        file_name=f"autoscore_perfiles_{datetime.date.today()}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# ── CERRAR SESIÓN ─────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
_c1, _c2, _c3 = st.columns([3,1,3])
with _c2:
    if st.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.rerun()

st.markdown("""
<div style="text-align:center;color:#ccc;font-size:0.65rem;margin-top:8px;">
    AutoScore AI — Dashboard F&I · Solo uso interno · Datos protegidos
</div>
""", unsafe_allow_html=True)
