import streamlit as st
from io import BytesIO
import base64
import os

def get_logo_b64():
    """Carga el logo como base64 para usar en HTML."""
    for name in ["AUTOSCOREIA.png", "logo_new.png", "logo.png"]:
        if os.path.exists(name):
            with open(name, "rb") as f:
                return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return ""

# ══════════════════════════════════════════
# PDF CLIENTE — incluido directamente
# ══════════════════════════════════════════
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from io import BytesIO

# ── PALETA ────────────────────────────────────────────────────────
AZUL_OSCURO   = HexColor("#050c1a")
AZUL_MEDIO    = HexColor("#0a1628")
AZUL_BORDE    = HexColor("#0e2040")
CYAN          = HexColor("#38bdf8")
CYAN_LIGHT    = HexColor("#7dd3fc")
MORADO        = HexColor("#8b5cf6")
VERDE         = HexColor("#22c55e")
AMARILLO      = HexColor("#eab308")
NARANJA       = HexColor("#f97316")
ROJO          = HexColor("#ef4444")
GRIS_TEXTO    = HexColor("#94a3b8")
GRIS_CLARO    = HexColor("#cbd5e1")
BLANCO        = HexColor("#f8fafc")
DORADO        = HexColor("#fbbf24")

W, H = letter  # 612 x 792 pts

# ── HELPERS ───────────────────────────────────────────────────────
def rect_fill(c, x, y, w, h, color):
    c.setFillColor(color)
    c.rect(x, y, w, h, fill=1, stroke=0)

def rect_stroke(c, x, y, w, h, color, line_w=0.5):
    c.setStrokeColor(color)
    c.setLineWidth(line_w)
    c.rect(x, y, w, h, fill=0, stroke=1)

def rounded_rect(c, x, y, w, h, r, fill_color=None, stroke_color=None, line_w=0.5):
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(line_w)
    c.roundRect(x, y, w, h, r,
                fill=1 if fill_color else 0,
                stroke=1 if stroke_color else 0)

def line_h(c, x1, x2, y, color, w=0.5):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.line(x1, y, x2, y)

def txt(c, text, x, y, font, size, color, align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "center":
        c.drawCentredString(x, y, text)
    elif align == "right":
        c.drawRightString(x, y, text)
    else:
        c.drawString(x, y, text)

def txt_wrap(c, text, x, y, max_w, font, size, color, line_h_pt=14):
    """Simple word-wrap."""
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    cy = y
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            c.drawString(x, cy, line)
            cy -= line_h_pt
            line = word
    if line:
        c.drawString(x, cy, line)
    return cy - line_h_pt  # y final

# ── MENSAJES PSICOLÓGICOS POR SCORE ───────────────────────────────
MENSAJES = {
    "AZUL": {
        "titulo":   "Tu camino hacia tu auto est\u00e1 listo",
        "subtitulo":"Perfil destacado",
        "cuerpo": (
            "Felicitaciones. Tu historial financiero refleja responsabilidad "
            "y compromiso, exactamente lo que las instituciones buscan. "
            "Eres un candidato prioritario para obtener las mejores condiciones "
            "de financiamiento disponibles en el mercado."
        ),
        "accion":   "El siguiente paso es simplemente agendar tu cita de formalización.",
        "urgencia": "Las unidades con mejores condiciones se apartan con anticipación.",
        "color":    CYAN,
        "icono":    "APROBADO",
    },
    "VERDE": {
        "titulo":   "Tu financiamiento est\u00e1 al alcance",
        "subtitulo":"Perfil favorable",
        "cuerpo": (
            "Tu situación financiera muestra solidez y buenos antecedentes. "
            "Con el proceso correcto, tienes altas posibilidades de obtener "
            "tu vehículo en las condiciones que necesitas. "
            "Estamos listos para acompañarte en cada paso."
        ),
        "accion":   "Podemos avanzar hoy mismo con tu proceso de aprobación.",
        "urgencia": "Asegurar tu unidad ahora te garantiza el precio y la disponibilidad.",
        "color":    VERDE,
        "icono":    "VIABLE",
    },
    "AMARILLO": {
        "titulo":   "Tu auto est\u00e1 m\u00e1s cerca de lo que crees",
        "subtitulo":"Perfil en proceso",
        "cuerpo": (
            "Hemos analizado tu situación y tenemos buenas noticias: "
            "existen caminos concretos para que puedas llevarte tu vehículo. "
            "Con ajustes menores en tu solicitud, tu perfil puede fortalecerse "
            "significativamente. Tu asesor tiene la estrategia perfecta para ti."
        ),
        "accion":   "Una conversación de 10 minutos con tu asesor puede cambiar el resultado.",
        "urgencia": "Cada día de espera puede significar cambios en tasas y disponibilidad.",
        "color":    AMARILLO,
        "icono":    "EN PROCESO",
    },
    "NARANJA": {
        "titulo":   "Encontramos la ruta para tu auto",
        "subtitulo":"Perfil con oportunidad",
        "cuerpo": (
            "Tu situación tiene solución. Contamos con opciones de financiamiento "
            "diseñadas específicamente para perfiles como el tuyo. "
            "No es un no, es un 'todavía no con este camino' — y tenemos "
            "el camino correcto para llevarte a donde quieres llegar."
        ),
        "accion":   "Tu asesor tiene alternativas específicas preparadas para ti.",
        "urgencia": "El momento de actuar es ahora, antes de que cambien las condiciones.",
        "color":    NARANJA,
        "icono":    "CON OPCION",
    },
    "ROJO": {
        "titulo":   "Tu soluci\u00f3n de movilidad existe",
        "subtitulo":"Plan de acci\u00f3n personalizado",
        "cuerpo": (
            "Entendemos que cada situación financiera es única y tiene su historia. "
            "Lo importante no es dónde estás hoy, sino hacia dónde vas. "
            "Hemos diseñado un plan específico para ti que, paso a paso, "
            "te acercará a tener el vehículo que necesitas."
        ),
        "accion":   "Tu asesor tiene un plan de acción personalizado listo para explicarte.",
        "urgencia": "Dar el primer paso hoy te pone en ventaja para el momento correcto.",
        "color":    ROJO,
        "icono":    "PLAN ACTIVO",
    },
}

# ── GENERADOR PRINCIPAL ───────────────────────────────────────────
def generar_pdf_cliente(datos: dict) -> BytesIO:
    """
    datos debe tener:
      nombre, telefono, correo,
      asesor, telefono_asesor, correo_asesor, rfc,
      sc (AZUL/VERDE/AMARILLO/NARANJA/ROJO),
      prob, cap_pago, mensualidad,
      decision, condicionamientos (list),
      docs (list), plan, temp
    """
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setTitle("Tu Análisis de Financiamiento — AutoScore AI")

    sc        = datos.get("sc", "AMARILLO")
    msg       = MENSAJES.get(sc, MENSAJES["AMARILLO"])
    color_sc  = msg["color"]
    nombre    = datos.get("nombre", "Cliente") or "Cliente"
    prob      = datos.get("prob", 0)
    cap_pago  = datos.get("cap_pago", 0)
    mensual   = datos.get("mensualidad", 0)
    asesor    = datos.get("asesor", "") or ""
    tel_a     = datos.get("telefono_asesor", "") or ""
    correo_a  = datos.get("correo_asesor", "") or ""
    plan      = datos.get("plan", "")
    docs      = datos.get("docs", [])

    # ══════════════════════════════════════════
    # PÁGINA 1 — RESULTADO Y CIERRE EMOCIONAL
    # ══════════════════════════════════════════

    # — Fondo oscuro total
    rect_fill(c, 0, 0, W, H, AZUL_OSCURO)

    # — Franja superior degradada
    rect_fill(c, 0, H-90, W, 90, AZUL_MEDIO)

    # — Línea top degradada (simulada con rectángulo delgado)
    rect_fill(c, 0, H-2, W, 2, CYAN)

    # — LOGO área (texto si no hay imagen)
    txt(c, "AutoScore AI", 40, H-38, "Helvetica-Bold", 16, CYAN)
    txt(c, "Aprobacion Inteligente", 40, H-52, "Helvetica", 8, GRIS_TEXTO)

    # — Línea separadora header
    line_h(c, 40, W-40, H-65, HexColor("#0e2040"), 0.8)

    # — Fecha y folio
    import datetime
    fecha = datetime.date.today().strftime("%d / %m / %Y")
    txt(c, f"Fecha: {fecha}", W-40, H-38, "Helvetica", 8, GRIS_TEXTO, "right")
    txt(c, "Analisis de Financiamiento Automotriz", W-40, H-52, "Helvetica", 7, HexColor("#334155"), "right")

    # — NOMBRE DEL CLIENTE grande
    nombre_upper = nombre.upper()
    txt(c, "Estimado(a),", 40, H-105, "Helvetica", 10, GRIS_TEXTO)
    txt(c, nombre_upper, 40, H-125, "Helvetica-Bold", 22, BLANCO)
    line_h(c, 40, 40 + c.stringWidth(nombre_upper, "Helvetica-Bold", 22), H-130, color_sc, 1.5)

    # — BADGE DE RESULTADO
    badge_x, badge_y, badge_w, badge_h = W-180, H-140, 140, 36
    rounded_rect(c, badge_x, badge_y, badge_w, badge_h, 6,
                 fill_color=HexColor("#0a1628"), stroke_color=color_sc, line_w=1)
    txt(c, msg["icono"], badge_x + badge_w/2, badge_y + 22, "Helvetica-Bold", 9, color_sc, "center")
    txt(c, msg["subtitulo"], badge_x + badge_w/2, badge_y + 9, "Helvetica", 7, GRIS_TEXTO, "center")

    # ── SECCIÓN: TÍTULO EMOCIONAL ──────────────────────────────────
    txt(c, msg["titulo"], 40, H-165, "Helvetica-Bold", 18, BLANCO)
    line_h(c, 40, 260, H-172, color_sc, 2)

    # ── CUERPO DEL MENSAJE ─────────────────────────────────────────
    final_y = txt_wrap(c, msg["cuerpo"], 40, H-195,
                       W-80, "Helvetica", 10, GRIS_CLARO, line_h_pt=16)

    # ── CITA DE ACCIÓN ─────────────────────────────────────────────
    accion_y = final_y - 18
    rounded_rect(c, 40, accion_y - 28, W-80, 42, 8,
                 fill_color=HexColor("#0a1e38"),
                 stroke_color=HexColor("#0e2a50"), line_w=0.8)
    # borde izq de color
    rect_fill(c, 40, accion_y - 28, 3, 42, color_sc)
    txt_wrap(c, f"  {msg['accion']}", 50, accion_y - 4,
             W-100, "Helvetica-Oblique", 10, CYAN_LIGHT, line_h_pt=14)

    # ── MÉTRICAS PRINCIPALES ───────────────────────────────────────
    met_y = accion_y - 72
    txt(c, "Tu analisis personalizado", 40, met_y + 12, "Helvetica-Bold", 9, CYAN)
    line_h(c, 40, W-40, met_y + 6, HexColor("#0e2040"), 0.5)

    # 3 cajas de métricas
    box_w = (W - 80 - 20) / 3
    boxes = [
        ("Probabilidad de aprobacion", f"{prob}%", color_sc),
        ("Capacidad de pago estimada", f"${cap_pago:,.0f}", CYAN_LIGHT),
        ("Mensualidad estimada", f"${mensual:,.0f}", HexColor("#a5b4fc")),
    ]
    for i, (lbl, val, col) in enumerate(boxes):
        bx = 40 + i * (box_w + 10)
        by = met_y - 62
        rounded_rect(c, bx, by, box_w, 55, 8,
                     fill_color=HexColor("#080f20"),
                     stroke_color=HexColor("#0e2040"), line_w=0.8)
        # top accent line
        rect_fill(c, bx, by + 53, box_w, 2, col)
        txt(c, lbl, bx + box_w/2, by + 38, "Helvetica", 7, GRIS_TEXTO, "center")
        txt(c, val, bx + box_w/2, by + 16, "Helvetica-Bold", 16, col, "center")

    # ── URGENCIA / LLAMADA A ACCIÓN ────────────────────────────────
    urg_y = met_y - 90
    rounded_rect(c, 40, urg_y - 32, W-80, 46, 8,
                 fill_color=HexColor("#12071e"),
                 stroke_color=MORADO, line_w=0.8)
    txt(c, "⏰  " + msg["urgencia"], W/2, urg_y - 8,
        "Helvetica-Bold", 9, DORADO, "center")
    txt(c, "Habla hoy con tu asesor para asegurar tu unidad y condiciones",
        W/2, urg_y - 22, "Helvetica", 8, GRIS_TEXTO, "center")

    # ── DOCUMENTACIÓN RÁPIDA ───────────────────────────────────────
    doc_y = urg_y - 58
    txt(c, "Documentacion que necesitas tener lista:",
        40, doc_y, "Helvetica-Bold", 9, CYAN)
    doc_x = 40
    doc_row_y = doc_y - 14
    for i, doc in enumerate(docs[:6]):
        col_offset = (i % 3) * (W/3)
        row_offset = (i // 3) * 14
        rounded_rect(c, 40 + col_offset, doc_row_y - row_offset - 12,
                     (W-80)/3 - 8, 13, 3,
                     fill_color=HexColor("#080f20"),
                     stroke_color=HexColor("#0e2040"), line_w=0.5)
        txt(c, f"  ✓  {doc}",
            44 + col_offset, doc_row_y - row_offset - 3,
            "Helvetica", 7.5, GRIS_CLARO)

    # ── SIGUIENTE PASO ─────────────────────────────────────────────
    paso_y = doc_row_y - 46
    anticipo = "Solicitar tu ENGANCHE COMPLETO" if plan == "DIRECTO" else "Apartar tu unidad con $5,000"
    rounded_rect(c, 40, paso_y - 28, W-80, 42, 8,
                 fill_color=HexColor("#0d1f0d"),
                 stroke_color=VERDE, line_w=1)
    txt(c, f"Siguiente paso:  {anticipo}",
        W/2, paso_y - 5, "Helvetica-Bold", 10, VERDE, "center")
    txt(c, "Cuenta BBVA  |  DAOSA SA DE CV  |  012320001250476847",
        W/2, paso_y - 19, "Helvetica", 8, GRIS_TEXTO, "center")

    # ── FOOTER PÁGINA 1 ────────────────────────────────────────────
    footer_y = 38
    line_h(c, 40, W-40, footer_y + 18, HexColor("#0e2040"), 0.5)
    txt(c, "Este documento es informativo. La aprobacion final depende de la evaluacion de la institucion financiera.",
        W/2, footer_y + 5, "Helvetica", 6.5, HexColor("#1e3a4a"), "center")
    txt(c, "AutoScore AI  —  Aprobacion Inteligente",
        W/2, footer_y - 6, "Helvetica", 6.5, HexColor("#1e3a4a"), "center")
    txt(c, "1", W-40, footer_y - 6, "Helvetica", 7, HexColor("#1e3a4a"), "right")

    c.showPage()

    # ══════════════════════════════════════════
    # PÁGINA 2 — DATOS DE CONTACTO Y CIERRE
    # ══════════════════════════════════════════

    rect_fill(c, 0, 0, W, H, AZUL_OSCURO)
    rect_fill(c, 0, H-60, W, 60, AZUL_MEDIO)
    rect_fill(c, 0, H-2, W, 2, CYAN)

    txt(c, "AutoScore AI", 40, H-28, "Helvetica-Bold", 13, CYAN)
    txt(c, "Tu asesor de confianza", W-40, H-28, "Helvetica", 8, GRIS_TEXTO, "right")
    line_h(c, 40, W-40, H-45, HexColor("#0e2040"), 0.5)

    # ── DATOS DEL ASESOR ──────────────────────────────────────────
    ase_y = H - 90
    txt(c, "Tu Asesor Especializado", 40, ase_y, "Helvetica-Bold", 14, BLANCO)
    line_h(c, 40, 220, ase_y - 6, CYAN, 1.5)

    # Card asesor
    card_h = 100
    rounded_rect(c, 40, ase_y - card_h - 12, W-80, card_h, 10,
                 fill_color=HexColor("#080f20"),
                 stroke_color=HexColor("#0e2040"), line_w=0.8)
    rect_fill(c, 40, ase_y - 14, 3, card_h, CYAN)

    iy = ase_y - 32
    txt(c, asesor or "Asesor AutoScore", 60, iy, "Helvetica-Bold", 14, BLANCO)
    txt(c, "Especialista en Financiamiento Automotriz", 60, iy - 14, "Helvetica", 8, CYAN_LIGHT)

    # íconos de contacto
    contactos = [
        ("TEL:", tel_a or "—"),
        ("EMAIL:", correo_a or "—"),
        ("RFC:", datos.get("rfc","") or "—"),
    ]
    for j, (lbl, val) in enumerate(contactos):
        cy2 = iy - 34 - j * 15
        txt(c, lbl, 60, cy2, "Helvetica-Bold", 8, GRIS_TEXTO)
        txt(c, val, 100, cy2, "Helvetica", 8, GRIS_CLARO)

    # ── COMPROMISO DE SERVICIO ─────────────────────────────────────
    comp_y = ase_y - card_h - 46
    txt(c, "Nuestro Compromiso Contigo", 40, comp_y, "Helvetica-Bold", 12, BLANCO)
    line_h(c, 40, 235, comp_y - 6, MORADO, 1.5)

    compromisos = [
        ("Transparencia total", "Te explicamos cada paso del proceso sin letra chica."),
        ("Opciones reales",     "Trabajamos con multiples financieras para encontrar la mejor opcion."),
        ("Acompanamiento",      "Tu asesor estara contigo desde la solicitud hasta la entrega."),
        ("Velocidad",           "Procesos agiles para que tengas tu auto en el menor tiempo posible."),
    ]
    for k, (titulo, desc) in enumerate(compromisos):
        ky = comp_y - 28 - k * 38
        rounded_rect(c, 40, ky - 26, W-80, 34, 6,
                     fill_color=HexColor("#070e1c"),
                     stroke_color=HexColor("#0a1628"), line_w=0.5)
        # bullet
        c.setFillColor(CYAN)
        c.circle(54, ky - 8, 3, fill=1, stroke=0)
        txt(c, titulo, 64, ky - 4, "Helvetica-Bold", 9, BLANCO)
        txt(c, desc, 64, ky - 16, "Helvetica", 8, GRIS_TEXTO)

    # ── MENSAJE DE CIERRE FINAL ────────────────────────────────────
    cierre_y = comp_y - 28 - 4 * 38 - 20

    rounded_rect(c, 40, cierre_y - 52, W-80, 66, 10,
                 fill_color=HexColor("#0d0719"),
                 stroke_color=MORADO, line_w=1)
    rect_fill(c, 40, cierre_y - 52, W-80, 2, MORADO)

    cierres = {
        "AZUL":     "Tu auto ideal te espera. Solo es cuestion de dar el siguiente paso.",
        "VERDE":    "Tienes todo lo necesario. Hagamos realidad este proyecto juntos.",
        "AMARILLO": "El camino esta trazado. Con el apoyo correcto, tu auto esta cerca.",
        "NARANJA":  "Cada desafio tiene solucion. Trabajemos juntos para encontrar la tuya.",
        "ROJO":     "El primer paso es el mas importante. Empieza hoy y cambia tu historia.",
    }
    txt(c, cierres.get(sc, cierres["AMARILLO"]),
        W/2, cierre_y - 20, "Helvetica-BoldOblique", 11, BLANCO, "center")
    txt(c, "— Tu equipo AutoScore AI",
        W/2, cierre_y - 38, "Helvetica-Oblique", 9, CYAN_LIGHT, "center")

    # ── FOOTER PÁGINA 2 ────────────────────────────────────────────
    line_h(c, 40, W-40, 56, HexColor("#0e2040"), 0.5)
    txt(c, "DAOSA SA DE CV  |  BBVA: 012320001250476847",
        W/2, 42, "Helvetica", 7, GRIS_TEXTO, "center")
    txt(c, "Este analisis es informativo. La aprobacion final depende de la evaluacion de la institucion financiera.",
        W/2, 30, "Helvetica", 6.5, HexColor("#1e3a4a"), "center")
    txt(c, "2", W-40, 30, "Helvetica", 7, HexColor("#1e3a4a"), "right")

    c.showPage()
    c.save()
    buf.seek(0)
    return buf


# ══════════════════════════════════════════
# APP PRINCIPAL
# ══════════════════════════════════════════
st.set_page_config(page_title="AutoScore AI", page_icon="🚗", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Exo+2:wght@300;400;500;600;700&display=swap');

/* ══════════════════════════════════════════
   NISSAN BRAND PALETTE
   Rojo #c3002f · Negro #000 · Blanco #fff
   Gris form #f5f5f5 · Gris card #1a1a1a
══════════════════════════════════════════ */

/* ─── BASE ─────────────────────────────── */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], section.main {
    background: #f5f5f5 !important;
    color: #111 !important;
}
[data-testid="stAppViewContainer"]::before {
    content: ""; position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(195,0,47,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(195,0,47,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none; z-index: 0;
}
.block-container {
    position: relative; z-index: 1;
    padding: 0 1.5rem 2rem 1.5rem !important;
    max-width: 100% !important;
}
/* Separación entre sec-label y primer input */
.sec-label + div,
.sec-label + [data-testid="stHorizontalBlock"] {
    margin-top: 8px !important;
}
*, *::before, *::after {
    font-family: 'Exo 2', sans-serif !important;
    box-sizing: border-box;
}

/* ─── TOPBAR ────────────────────────────── */
.topbar-wrap {
    background: #000;
    padding: 10px 24px;
    display: flex; align-items: center; gap: 14px;
    margin: 0 -1.5rem;
    min-height: 72px;
}
.topbar-title {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.4rem; font-weight: 700;
    color: #ffffff; letter-spacing: 0.1em; line-height: 1;
}
.topbar-sub {
    color: #c3002f; font-size: 0.6rem;
    letter-spacing: 0.18em; text-transform: uppercase; margin-top: 2px;
}
.topbar-divider {
    display: inline-block; width: 1px; height: 34px;
    background: #222; margin: 0 14px; vertical-align: middle;
}
.topbar-desc { color: #555; font-size: 0.68rem; letter-spacing: 0.04em; }
.topbar-badge {
    background: rgba(195,0,47,0.12);
    border: 1px solid rgba(195,0,47,0.3);
    border-radius: 50px; padding: 4px 12px;
    font-size: 0.6rem; color: #c3002f;
    letter-spacing: 0.1em; text-transform: uppercase; font-weight: 600;
}

/* ─── SECTION LABEL ─────────────────────── */
.sec-label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.68rem; font-weight: 700;
    color: #c3002f; text-transform: uppercase;
    letter-spacing: 0.14em; margin: 22px 0 10px;
    display: flex; align-items: center; gap: 7px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(195,0,47,0.2);
}
.sec-label:first-child { margin-top: 16px; }

/* ─── PANEL FORMULARIO — gris claro ──────── */
/* Panel izquierdo — blanco */
[data-testid="column"]:first-child {
    background: #ffffff !important;
    border-right: 1px solid #e0e0e0 !important;
    padding: 0 16px 16px 0 !important;
}
[data-testid="column"]:first-child .sec-label {
    color: #c3002f !important;
    border-bottom-color: rgba(195,0,47,0.2) !important;
}
[data-testid="column"]:first-child label,
[data-testid="column"]:first-child [data-testid="stWidgetLabel"] p {
    color: #c3002f !important;
}
/* Panel derecho — negro */
[data-testid="column"]:last-child {
    background: #0d0d0d !important;
    padding: 0 0 16px 16px !important;
}
[data-testid="column"]:last-child label,
[data-testid="column"]:last-child [data-testid="stWidgetLabel"] p {
    color: #555 !important;
}

/* ─── INPUTS ────────────────────────────── */
.stTextInput input, .stNumberInput input {
    background: #ffffff !important;
    color: #111 !important;
    border: 1px solid #ddd !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    font-size: 0.82rem !important;
    width: 100% !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #c3002f !important;
    box-shadow: 0 0 0 2px rgba(195,0,47,0.12) !important;
}
.stTextInput input::placeholder, .stNumberInput input::placeholder {
    color: #bbb !important;
}
.stSelectbox > div > div {
    background: #ffffff !important;
    color: #111 !important;
    border: 1px solid #ddd !important;
    border-radius: 8px !important;
    padding: 2px 8px !important;
    font-size: 0.82rem !important;
}
label, [data-testid="stWidgetLabel"] p {
    color: #c3002f !important;
    font-size: 0.65rem !important; font-weight: 600 !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    margin-bottom: 2px !important;
}
.stNumberInput button {
    background: #f5f5f5 !important;
    border: 1px solid #ddd !important;
    color: #c3002f !important; border-radius: 6px !important;
    padding: 2px 8px !important; width: auto !important; margin: 0 !important;
}
/* Grid pattern solo en fondo gris — no en panels */
[data-testid="stAppViewContainer"]::before { display: none !important; }
div[data-testid="stVerticalBlock"] { gap: 0.28rem !important; }

/* ─── BOTÓN PRINCIPAL ────────────────────── */
.stFormSubmitButton > button, .stButton > button {
    width: 100% !important;
    background: #c3002f !important;
    color: #fff !important; border: none !important;
    border-radius: 50px !important; padding: 12px 24px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem !important; font-weight: 700 !important;
    letter-spacing: 0.13em !important; text-transform: uppercase !important;
    box-shadow: 0 4px 20px rgba(195,0,47,0.35) !important;
    margin-top: 6px !important;
    transition: transform 0.15s, box-shadow 0.15s, background 0.15s !important;
}
.stFormSubmitButton > button:hover, .stButton > button:hover {
    background: #e8001a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(195,0,47,0.5) !important;
}

/* ─── ALERTS ──────────────────────────────── */
.stSuccess > div {
    background: #f0fdf4 !important; border: 1px solid #bbf7d0 !important;
    border-radius: 9px !important; color: #166534 !important; font-size: 0.82rem !important;
}
.stWarning > div {
    background: #fffbeb !important; border: 1px solid #fde68a !important;
    border-radius: 9px !important; color: #92400e !important; font-size: 0.82rem !important;
}
.stError > div {
    background: #fff1f2 !important; border: 1px solid #fecdd3 !important;
    border-radius: 9px !important; color: #9f1239 !important; font-size: 0.82rem !important;
}
.stInfo > div {
    background: #f8f9fa !important; border: 1px solid #e2e8f0 !important;
    border-radius: 9px !important; color: #334155 !important; font-size: 0.82rem !important;
}

hr { border:none !important; border-top:1px solid #1a1a1a !important; margin:8px 0 !important; }
.stCaption p { color:#c3002f !important; font-size:0.72rem !important; }

.stLinkButton a {
    background: #1a1a1a !important; border: 1px solid #333 !important;
    color: #fff !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 0.8rem !important;
    width: 100% !important; display: block !important;
    text-align: center !important; padding: 9px !important;
}
.stDownloadButton > button {
    background: #1a1a1a !important; border: 1px solid #c3002f !important;
    color: #c3002f !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 0.8rem !important;
    width: 100% !important; padding: 9px !important;
}

/* ─── EXPANDER ────────────────────────────── */
[data-testid="stExpander"] {
    background: #111 !important;
    border: 1px solid #222 !important;
    border-radius: 10px !important; overflow: visible !important;
}
[data-testid="stExpander"] details { background: transparent !important; }
[data-testid="stExpander"] details summary {
    background: #111 !important; border-radius: 10px !important;
    padding: 10px 14px !important; cursor: pointer !important;
    position: relative !important; z-index: 1 !important;
}
[data-testid="stExpander"] details summary::marker,
[data-testid="stExpander"] details summary::-webkit-details-marker {
    display: none !important; content: "" !important;
}
[data-testid="stExpander"] details summary p,
[data-testid="stExpander"] details summary div,
[data-testid="stExpander"] details summary span {
    color: #888 !important; font-size: 0.78rem !important;
    font-weight: 600 !important; background: transparent !important;
    border: none !important; box-shadow: none !important;
}
[data-testid="stExpander"] details > div {
    background: #0d0d0d !important;
    border-top: 1px solid #222 !important;
    padding: 12px 14px !important;
    border-radius: 0 0 10px 10px !important;
    position: relative !important; z-index: 0 !important;
}
[data-testid="stExpander"] details > div * { background: transparent !important; box-shadow: none !important; }
[data-testid="stExpander"] svg { color: #555 !important; fill: #555 !important; }

/* ─── RESULTADO UI ────────────────────────── */
.prob-hero {
    display: flex; align-items: flex-end; gap: 10px;
    padding: 16px 20px 12px;
    background: #000;
    border: 1px solid #1a1a1a;
    border-radius: 14px; margin-bottom: 10px;
    position: relative; overflow: hidden;
}
.prob-hero::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: #c3002f;
}
.prob-label { font-size: 0.7rem; color: #555; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; }
.prob-sublabel { font-family: 'Rajdhani', sans-serif !important; font-size: 0.82rem; color: #444; letter-spacing: 0.04em; }

.score-badge {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 10px 16px; border-radius: 12px; margin: 6px 0; width: 100%;
}
.score-badge .score-em  { font-size: 1.5rem; }
.score-badge .score-lbl { font-family: 'Rajdhani', sans-serif !important; font-size: 1.1rem; font-weight: 700; letter-spacing: 0.06em; }
.score-badge .score-sub { font-size: 0.72rem; color: #444; margin-top: 1px; }

.metrics-2 { display: flex; gap: 10px; margin: 8px 0; }
.metric-tile { flex: 1; border-radius: 10px; padding: 10px 14px; }
.metric-tile.blue   { background: #000; border: 1px solid #1a1a1a; }
.metric-tile.purple { background: #1a0006; border: 1px solid rgba(195,0,47,0.25); }
.metric-tile .mt-lbl { font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; font-weight: 600; }
.metric-tile.blue   .mt-lbl { color: #555; }
.metric-tile.purple .mt-lbl { color: #c3002f; }
.metric-tile .mt-val { font-family: 'Rajdhani', sans-serif !important; font-size: 1.35rem; font-weight: 700; color: #fff; line-height: 1; }

.semaforo {
    display: flex; align-items: center; justify-content: center;
    gap: 10px; padding: 10px 16px; border-radius: 10px;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase; margin: 8px 0;
}
.semaforo.verde    { background:#f0fdf4; border:1px solid #bbf7d0; color:#166534; }
.semaforo.amarillo { background:#fffbeb; border:1px solid #fde68a; color:#92400e; }
.semaforo.naranja  { background:#fff7ed; border:1px solid #fed7aa; color:#9a3412; }
.semaforo.rojo     { background:#fff1f2; border:1px solid #fecdd3; color:#9f1239; }

.msg-cliente {
    background: #0d0d0d; border: 1px solid #1a1a1a;
    border-left: 3px solid #c3002f; border-radius: 0 9px 9px 0;
    padding: 10px 14px; color: #aaa;
    font-size: 0.8rem; line-height: 1.6; margin: 6px 0;
}

.estrategia-box {
    background: #1a0006; border: 1px solid rgba(195,0,47,0.25);
    border-left: 3px solid #c3002f; border-radius: 0 9px 9px 0;
    padding: 10px 14px; color: #f87171;
    font-size: 0.78rem; line-height: 1.6;
}

.sec-label-result {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.68rem; font-weight: 700; color: #555;
    text-transform: uppercase; letter-spacing: 0.14em;
    margin: 10px 0 5px; display: flex; align-items: center; gap: 7px;
    padding-bottom: 5px; border-bottom: 1px solid #1a1a1a;
}

.alerta-chip {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 11px; border-radius: 7px;
    font-size: 0.74rem; font-weight: 600;
    margin: 3px 0; letter-spacing: 0.02em;
}
.alerta-chip.ok  { background:#f0fdf4; border:1px solid #bbf7d0; color:#166534; }
.alerta-chip.bad { background:#fff1f2; border:1px solid #fecdd3; color:#9f1239; }

.cond-box {
    background: #fffbeb; border: 1px solid #fde68a;
    border-radius: 9px; padding: 10px 14px;
    color: #92400e; font-size: 0.76rem;
    line-height: 1.75; margin: 4px 0; font-weight: 500;
}

.cuenta-box {
    background: #000; border: 1px solid #1a1a1a;
    border-top: 2px solid #c3002f;
    border-radius: 9px; padding: 10px 14px; margin: 4px 0;
}

.security-line {
    text-align: center; color: #333; font-size: 0.68rem;
    letter-spacing: 0.06em; margin-top: 8px;
    display: flex; align-items: center; justify-content: center; gap: 5px;
}

/* Botón notas internas — alineado como fila de alerta */
div[data-testid="stButton"]:has(button[key="btn_estrategia"]) {
    width: 100% !important;
}
div[data-testid="stButton"]:has(button[key="btn_estrategia"]) > button {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    color: #555 !important;
    border-radius: 7px !important;
    padding: 6px 11px !important;
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    text-transform: none !important;
    box-shadow: none !important;
    width: 100% !important;
    text-align: left !important;
    margin: 3px 0 !important;
}
div[data-testid="stButton"]:has(button[key="btn_estrategia"]) > button:hover {
    border-color: rgba(195,0,47,0.4) !important;
    color: #888 !important;
    background: #161616 !important;
    transform: none !important;
    box-shadow: none !important;
}

.panel-left  { border-right: 1px solid #1a1a1a; padding-right: 16px; }
.panel-right { padding-left: 16px; }
</style>
""", unsafe_allow_html=True)

# ── LOGO BASE64 ────────────────────────────────────────────────────
_LOGO_SRC = get_logo_b64()

# ── SESSION STATE ──────────────────────────────────────────────────
for k, v in {
    "resultado": None, "cotitular_activo": False,
    "cotitular_resultado": None, "ingreso": 0.0, "mensualidad": 0.0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── TOPBAR — título centrado, sin imagen problemática ──────────────
st.markdown(f"""
<div class="topbar-wrap">
  <img src="{_LOGO_SRC}" height="52"
       style="flex-shrink:0;object-fit:contain;margin-left:8px;">
  <div style="margin-left:auto;display:flex;align-items:center;gap:20px;">
    <span style="color:#555;font-size:0.72rem;letter-spacing:0.04em;">Herramienta de Pre-Análisis de Crédito Automotriz</span>
    <span class="topbar-badge">🔒 Datos protegidos</span>
  </div>
</div>
<div style="height:2px;margin:0 -1.5rem 0;background:#c3002f;"></div>
""", unsafe_allow_html=True)

# ── DOS COLUMNAS ───────────────────────────────────────────────────
col_izq, col_der = st.columns([1, 1], gap="medium")

# ╔══════════════════════════════════╗
# ║      IZQUIERDA — FORMULARIO      ║
# ╚══════════════════════════════════╝
with col_izq:

    # LOGO arriba del formulario — izquierda
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
            justify-content:center;min-height:55vh;gap:20px;padding:20px 0;">
          <img src="" + _LOGO_SRC + ""
               style="width:260px;max-width:90%;object-fit:contain;"
               onerror="this.style.display='none'"/>
          <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;
              color:#111;text-transform:uppercase;letter-spacing:0.12em;text-align:center;">
              Resultado del Análisis
          </div>
          <div style="font-size:0.72rem;color:#999;letter-spacing:0.08em;
              text-transform:uppercase;text-align:center;margin-top:-12px;">
              Completa el formulario y presiona Analizar
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
        st.markdown('<div class="sec-label-result">⚠️ Riesgos detectados</div>', unsafe_allow_html=True)
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

        lbl_btn = "🔒 Notas internas — solo asesor" if not st.session_state.mostrar_estrategia else "🔒 Cerrar notas internas"
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
            st.markdown('<div class="sec-label-result">📋 Condicionamientos</div>', unsafe_allow_html=True)
            cond_items = "".join([f"• {c}<br>" for c in r["condicionamientos"]])
            st.markdown(f'<div class="cond-box">{cond_items}</div>', unsafe_allow_html=True)

        # ── 8. DOCUMENTACIÓN ─────────────────────────────────
        st.markdown('<div class="sec-label-result">📄 Documentación requerida</div>', unsafe_allow_html=True)
        docs_chips = " &nbsp;·&nbsp; ".join([f"📎 {d}" for d in r["docs"]])
        st.markdown(f'<div style="color:#64748b;font-size:0.76rem;padding:4px 2px;">{docs_chips}</div>', unsafe_allow_html=True)

        # ── 9. SIGUIENTE PASO + CUENTA ────────────────────────
        st.markdown('<div class="sec-label-result">💰 Siguiente paso</div>', unsafe_allow_html=True)
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
            st.markdown('<div class="sec-label-result">👥 Análisis de Cotitular</div>', unsafe_allow_html=True)
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


        # ── PDF CLIENTE ─────────────────────────────────────────────
        st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)
        ok = all([r.get("asesor","").strip(), r.get("nombre","").strip(), r.get("telefono","").strip()])
        if not ok:
            st.warning("⚠️ Completa datos de asesor y cliente para generar PDF")
        else:
            buf_pdf = generar_pdf_cliente(r)
            st.download_button(
                "📄 Descargar PDF para el cliente",
                data=buf_pdf.getvalue(),
                file_name=f"autoscore_{(r.get('nombre','cliente') or 'cliente').replace(' ','_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        st.markdown('<div class="security-line">🛡️ Datos protegidos y seguros</div>', unsafe_allow_html=True)
