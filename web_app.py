import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Perfilador PRO", layout="centered")
st.markdown("""
<style>
/* FONDO TECNOLÓGICO */
html, body, .stApp {
   background: radial-gradient(circle at top, #0f172a, #020617);
   color: white;
}
/* HERO SECTION */
.hero {
    text-align: center;
    padding-top: 40px;
    padding-bottom: 20px;
}
/* LOGO GRANDE + GLOW */
.hero img {
    width: 420px;
    filter: drop-shadow(0px 0px 60px rgba(56,189,248,0.9));
}
/* EFECTO LUZ ABAJO */
.glow-line {
    width: 60%; 
    height: 3px;
    margin: 25px auto;
    background: linear-gradient(90deg, transparent, #38bdf8, transparent);
    box-shadow: 0px 0px 20px #38bdf8;
    border-radius: 50%;
}                                                                                                                                                                                                 
/* CONTENEDOR */
.block-container {
    padding-top: 0rem;
    max-width: 900px;      
}
/* INPUTS */
.stTextInput input,
.stNumberInput input,
.stSelectbox div {
   background-color: #111827 !important;
   color: white !important;
   border-radius: 10px;
   border: 1px solid #1f2937;
}
/* LABELS */
label {
    color: #9ca3af !important;
}
</style>                                                         
""", unsafe_allow_html=True)

# HERO VISUAL
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("logo_new.png", width=620)
    
    st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)    
# =========================
# SESSION
# =========================
if "resultado" not in st.session_state:
    st.session_state.resultado = None

if "cotitular_activo" not in st.session_state:
    st.session_state.cotitular_activo = False

if "cotitular_resultado" not in st.session_state:
  st.session_state.cotitular_resultado = None

if "analizado" not in st.session_state:
    st.session_state.analizado = False
# =========================      
# 👤 ASESOR
# =========================
st.markdown("# 👤 Datos del asesor")

asesor = st.text_input("Nombre asesor")
telefono_asesor = st.text_input("Teléfono asesor")
correo_asesor = st.text_input("Correo asesor")
rfc = st.text_input("RFC asesor")
st.divider()

# =========================
# 👥 CLIENTE
# =========================
st.markdown("## 👥 Datos del cliente")
nombre_cliente = st.text_input("Nombre cliente")
telefono = st.text_input("Teléfono")
correo = st.text_input("Correo")

     
with st.form("formulario"):
    st.markdown("## 📊 Perfil del cliente")

    edad = st.number_input("Edad", 18, 73, 18)

    ingreso = st.number_input(
        "Ingreso mensual",
        min_value=6500.0,
        value=6500.0,
        step=500.0,
        format="%.2f"
    )
    tipo_ingreso = st.selectbox(
        "Tipo de ingreso",
        ["Nómina", "Independiente", "No comprueba ingresos"],
        key="tipo_ingreso"
    )    
   
    
    negocio_casa = st.selectbox(
        "¿Negocio en domicilio?",
        [1, 2],
        format_func=lambda x: "Sí" if x == 1 else "No",
    )    
    # ⚠️ aviso visual (UX)
    if tipo_ingreso != "Independiente":
      st.caption("⚠️ Solo aplica para independientes")    
     
 
    domicilio = st.selectbox(
          "Antigüedad domicilio", 
          [1,2,3],
          format_func=lambda x: ["<1 año","1-3 años","+3 años"][x-1]
    )

    domicilio_buro = st.selectbox(
          "¿Tu domicilio coincide con identificaciones?",
          [1,2],
          format_func=lambda x: "Sí" if x==1 else "No"
    )

    precio = st.number_input("Precio vehículo", format="%0.2f")
    enganche = st.number_input("Enganche", format="%0.2f")

    consultas = st.number_input("Consultas o creditos recientes (últimos 3 meses)", 0, 20)
    plazo = st.selectbox("Plazo", [12,24,36,48,60,72])

    # =========================
    # HISTORIAL
    # =========================
    st.subheader("📊 Historial")

    auto = st.selectbox("Automotriz", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    credinissan = st.selectbox("CrediNissan", [1,2], format_func=lambda x: "Sí" if x==1 else "No")

    hipotecario = st.selectbox(
      "Hipotecario",
       [1,2,3],
       format_func=lambda x: ["Bancario","Infonavit","No tiene"][x-1]
    )

    tarjeta_alta = st.selectbox("Tarjetas mayores a 100 mil", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    tarjeta_baja = st.selectbox("Tarjetas menores a 100 mil o departamentales", [1,2], format_func=lambda x: "Sí" if x==1 else "No")

    atrasos = st.selectbox(
          "Atrasos", 
          [1,2,3],
          format_func=lambda x: ["1-30 dias","31 a 60","+ 61 dias"][x-1]
    )

    # =========================
    # PERFIL COMPRA
    # =========================
    st.subheader("🔥 Perfil compra")

    enganche_disp = st.selectbox("¿Tiene enganche?", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    compra_mes = st.selectbox("¿Compra este mes?", [1,2], format_func=lambda x: "Sí" if x==1 else "No")
    unidad = st.selectbox("¿Hay unidad?", [1,2], format_func=lambda x: "Sí" if x==1 else "No")

    submitted = st.form_submit_button("🔥ANALIZAR PERFIL")

# =========================
# ANALIZAR
# =========================

if submitted:
   st.session_state.analizado = True
   st.session_state.ingreso = ingreso
   # BASE
   monto = precio - enganche
   mensualidad = (monto/100000)*2200*(plazo/72)
   enganche_pct = (enganche/precio)*100 if precio>0 else 0
   
         
   # =========================
   # FILTRO DE RIESGO REAL
   # =========================

   riesgo_alto = False
   riesgo_medio = False 

   # 🔴 ATRASOS FUERTES
   if atrasos == 3:
       riesgo_alto = True
        
   # 🔴 MUCHAS CONSULTAS
   if consultas >= 8:
       riesgo_alto = True
   elif consultas >= 5: 
       riesgo_medio = True        

   # 🔴 INGRESO NO ESTABLE   
   if tipo_ingreso == "Independiente":
       riesgo_medio = True

   if tipo_ingreso == "No comprueba ingresos": 
        riesgo_alto = True   

    # 🔴 ENGANCHE BAJO (CLAVE)
   if enganche_pct < 20:
       riesgo_medio = True

   if enganche_pct < 10:
       riesgo_alto = True    

    # SCORE
   score = 0
        
   if tarjeta_alta == 1:
        score += 4
   if tarjeta_baja == 1 and ingreso > 30000:
        score += 1    
    # 🚗 CREDINISSANs    
   if credinissan == 1:
        score += 5
    # 🚗 CREDITO AUTOMOTRIZ GENERAL
   if auto == 1:
        score += 3
    # 🏦 HIPOTECARIO (menos peso para auto)
   if hipotecario == 1:
       score += 3
   elif hipotecario == 2: 
       score += 1
      
      
   #ATRASOS
   if atrasos == 2:          
      score -= 3
   elif atrasos == 3:     
        score -= 10
    # CONSULTAS    
   if consultas >= 8:     
       score -= 12
   elif consultas >= 5:     
      score -= 6
   elif consultas >= 3:
       score -= 3

    # PERFIL    
   if score <= 0:    
      perfil = "DELGADO"
   elif score >= 7:
      perfil = "FUERTE"
   else:
      perfil = "MEDIO"

   # PROBABILIDAD     
   if perfil == "FUERTE":     
      prob = 85
   elif perfil == "MEDIO":     
        prob = 65
   else:     
        prob = 30

   if enganche_pct >= 40:     
        prob += 10
   elif enganche_pct >= 25:     
        prob += 5

   if consultas >= 8:    
        prob -= 25
   elif consultas >= 5:
       prob -= 15
   elif consultas >= 3:
       prob -= 5    
   prob = max(5, min(95, prob))

   # =========================
   # CAPACIDAD DE PAGO    
   # =========================    
   capacidad_pago = 0

   if tipo_ingreso == "Nómina":
      capacidad_pago = ingreso / 2
   elif tipo_ingreso == "Independiente":    
      capacidad_pago = ingreso / 3.33     
   else:      
      capacidad_pago = ingreso / 3.33

   excede_capacidad = mensualidad > capacidad_pago           

   # TEMPERATURA     
   if compra_mes == 2:    
      temp = "❄️ FRÍO"
   elif compra_mes == 1 and enganche_disp == 1 and unidad == 1:    
      temp = "🔥 CALIENTE"
   else:
      temp = "🟡 TIBIO"

   # =========================     
   # SCORE COLOR     
   # =========================     

   if prob >= 80:     
      score_color = "AZUL"
   elif prob >= 70:     
      score_color = "VERDE"
   elif prob >= 45:
      score_color = "AMARILLO"
   elif prob >= 35:
      score_color = "NARANJA"
   else:
      score_color = "ROJO"
            
   # =========================     
   # DECISION PREDICTIVA REAL     
   # =========================     
   mensaje_cliente = ""
   mensaje_asesor = ""
   decision = "🟡 EN EVALUACIÓN"
   plan = "REVISION"

   if consultas >= 10:
       decision = "🟠 ESTRATEGIA ALTERNATIVA"
       plan = "COTITULAR"

    # 🔴 BLOQUEO TOTAL
   elif atrasos == 3:
        decision = "🟠 ESTRATEGIA ALTERNATIVA"
        plan = "ALTERNATIVA"
        
        mensaje_cliente = """Tu perfil puede avanzar mediante una alternativa de financiamiento."""
        mensaje_asesor = """Subir enganche / cotitular / evitar consultas"""


    # 🔴 SCORE MUY BAJO
   elif score_color == "ROJO":
        decision = "🟠 ESTRATEGIA ALTERNATIVA"
        plan = "COTITULAR"

        mensaje_cliente = """Tu perfil actualmente requiere una alternativa de financiamiento."""
        mensaje_asesor = """Buscar cotitular fuerte / Subir enganche / Evitar más consultas en buró."""
    
    # ⚠️ CAPACIDAD DE PAGO (CONDICIONA)
   elif excede_capacidad and prob < 70:
        decision = "🟡 AJUSTE NECESARIO"
        plan = "AJUSTAR_PLAZO"
            
        mensaje_cliente = """La mensualidad puede ajustarse para mejorar tu perfil."""
        mensaje_asesor = """Ampliar plazo / Reducir monto a financiar / Validar ingresos """
   
   # 🟠 RIESGO MEDIO (RESCATABLE)
   elif riesgo_medio and prob < 60:
        decision = "🟠 PERFIL CON OPORTUNIDAD"
        plan = "RESCATE"

        mensaje_cliente = """Tu perfil tiene alta posibilidad de avanzar ajustando algunos puntos clave."""
        mensaje_asesor = """ Subir enganche (ideal 25%+) / Buscar cotitular línea directa / Evitar más consultas en buró. """
    
   # 🟢 PROBABILIDAD ALTA
   elif prob >= 70:
      if riesgo_medio:
        decision = "🟢 APROBADO EN ANALISIS DE FIANCIERA"
        plan = "SE VA A ANALISIS"
              
        mensaje_cliente = """Tu perfil es viable y puede avanzar a proceso de aprobación, con validaciones normales."""
        mensaje_asesor = """Posible validación de ingresos / Investigacion telefónica"""
       
      else:
        decision = "🟢 APROBADO"
        plan = "AUTOMATICO"

        mensaje_cliente = """Tu perfil cumple con los criterios para avanzar en automatico."""
        mensaje_asesor = "Perfil limpio. Proceder directo."    

   # 🟡 PERFIL MEDIO
   elif prob >= 50:
       if enganche_pct < 20 or riesgo_medio:
         decision = "🟡 APROBABLE AJUSTES"
         plan = "CONDICIONADO"

         mensaje_cliente = """Tu perfil es viable realizando algunos ajustes."""

         mensaje_asesor = """ Subir enganche (+15 pts ideal) / Validacion por financiera."""
        
       else:
        decision = "🟡 PRE APROBADO"
        plan = "DIRECTO"

        mensaje_cliente = """Tu perfil es favorable para avanzar."""
        mensaje_asesor = "Perfil estable. Proceder."       

   # 🟡 PERFIL BAJO
   elif prob >= 35:
        decision = "🟡 PERFIL MEJORABLE"
        plan = "COTITULAR"

        mensaje_cliente = """Tu perfil puede fortalecerse con apoyo adicional."""
        mensaje_asesor = """Integrar cotitular fuerte / Comprobar ingresos / Mejorar enganche"""
   # 🔴 NO VIABLE
   else:
        decision = "🟠 ESTRATEGIA ALTERNATIVA"
        plan = "ALTERNATIVA"

        mensaje_cliente = """Tu perfil puede avanzar mediante una alternativa de financiamiento"""
        mensaje_asesor = """Financiera flexible / Reestructura de perfil."""

   # INVESTIGACIÓN
   investigacion = "🟢 Sin validaciones relevantes"

   if tipo_ingreso == "Independiente" and negocio_casa == 1:
       prob = max(prob, 80)
       investigacion = "🔴 Requiere validación física"

   elif tipo_ingreso == "Independiente":
       investigacion = "🟡 validacion de ingresos"
       
   elif domicilio_buro == 2:
       investigacion = "🔴 Validación de domicilio"

   elif tipo_ingreso != "Nómina" and prob < 45:
       investigacion = "🔴 Validación adicional requerida"

   # DOCUMENTOS
   documentos = ["INE", "Comprobante de domicilio"]
   
   if plan == "DIRECTO":
        documentos = ["INE", "Comprobante", "Cotización"]
   elif plan == "COTITULAR":
        documentos += ["Cotitular obligatorio"]
   elif tipo_ingreso == "Nómina":
        documentos += ["Nómina", "Estado de cuenta"]
   else:
        documentos += ["Estados de cuenta"]

   # =======================
   # RESULTADO PARA PDF
   # ======================
    
   r = {
       "nombre": nombre_cliente,
       "telefono": telefono,
       "correo": correo, 
       "perfil": perfil,
       "prob": prob,
       "decision": decision,
       "asesor": asesor,
       "telefono_asesor": telefono_asesor,
       "correo_asesor": correo_asesor,
       "rfc": rfc,
       "capacidad_pago": capacidad_pago,
       

   }    

   # GUARDAR      
   st.session_state.resultado = {    
       "perfil": perfil,
       "score_color": score_color,
       "prob": prob,
       "temp": temp,
       "investigacion": investigacion,
       "decision": decision,
       "plan": plan,
       "mensaje_cliente": mensaje_cliente,
       "mensaje_asesor": mensaje_asesor,

    # CLIENTE    
      "nombre": nombre_cliente,   
      "telefono": telefono,   
      "correo": correo,
   
   # ASESOR     
       "asesor": asesor,
       "telefono_asesor": telefono_asesor,
       "correo_asesor": correo_asesor,
       "rfc": rfc,
        
       "documentos": documentos,
       "mensualidad": mensualidad,
       "capacidad_pago": capacidad_pago,
       
   }

       
   st.session_state.cotitular_activo = (plan == "COTITULAR")
   st.session_state.cotitular_resultado = None

# =========================   
# RESULTADO   
# =========================   
if st.session_state.resultado:
   
   r = st.session_state.resultado

   st.subheader("📊 RESULTADO") 

   # =========================
   # 🟡 SCORE
   # =========================
   if r["score_color"] == "AZUL":
        score_label = "🔵 SCORE AZUL"
        score_desc = "Perfil fuerte, alta probabilidad de aprobación"
   elif r["score_color"] == "VERDE":
        score_label = "🟢 SCORE VERDE"
        score_desc = "Buen perfil, aprobado con condiciones normales"
   elif r["score_color"] == "AMARILLO":
        score_label = "🟡 SCORE AMARILLO"
        score_desc = "Perfil medio, requiere validación adicional"
   elif r["score_color"] == "NARANJA":
       score_label = "🟠 SCORE NARANJA"
       score_desc = "Perfil débil, requiere estructura (cotitular/enganche)"           
   else:
       score_label = "🟠 PERFIL EN DESARROLLO"
       score_desc = "Perfil con oportunidad mediante estrategia alternativa" 

   st.subheader(score_label)
   st.write(score_desc)
   st.write(f"Probabilidad: {r['prob']}%")   
   # =========================
   # 💰 CAPACIDAD DE PAGO
   # =========================
   st.markdown(f"### 💰 Capacidad de pago: ${r['capacidad_pago']:,.0f}")
       
   # 🟢 DECISIÓN (INTELIGENTE)  
   if "APROBADO" in r["decision"]:
     st.success(r["decision"])
   elif "ALTERNATIVA" in r["decision"]:
           st.warning(r["decision"])
   elif "CONDICIONES" in r["decision"] or "AJUSTE" in r["decision"]:
           st.warning(r["decision"])    
   else:  
           st.error(r["decision"])      

    # 💡 MENSAJE CLIENTE (SOLO UNA VEZ)
   if r.get("mensaje_cliente"):
        st.markdown(f"""
            <div style="background-color:#f8fafc;
                    padding:15px;
                    border-radius:10px;
                    color:#0f172a;
                    border:1px solid #e2e8f0;">
            💡 {r['mensaje_cliente']}
            </div>
            """, unsafe_allow_html=True)
                        
       # 🔒 MENSAJE ASESOR     
   with st.expander("🔒 Estrategia interna"):
           st.write(r.get("mensaje_asesor", ""))
   # =========================
   # 🔎 INVESTIGACIÓN
   # =========================
   st.subheader("🔎 Validaciones")
   st.write(r["investigacion"])
   # =========================
   # 📄 DOCUMENTOS DOCUMENTOS
   # =========================
   st.subheader("📄 Documentación")
   for d in r["documentos"]:
       st.write(f"• {d}")
   
    # =========================
    # COTITULAR
    # =========================
   if st.session_state.cotitular_activo:
       
       st.subheader("👥 ANALIZAR COTITULAR")

       tipo_cot = st.selectbox("Tipo cotitular", ["Línea directa", "Conocido"])
       ingreso_cot = st.number_input("Ingreso cotitular")
       auto_cot = st.selectbox("Automotriz cotitular", ["Sí","No"])
       credinissan_cot = st.selectbox("CrediNissan cotitular", ["Sí","No"])
       hipotecario_cot = st.selectbox("Hipotecario cotitular", ["No tiene","Infonavit","Bancario"])
       tarjeta_alta_cot = st.selectbox("Tarjetas >100k cotitular", ["Sí","No"])
       atrasos_cot = st.selectbox(
           "Buró de crédito cotitular",
           ["Sin atrasos", "1-30 días", "31-60 días", "61+ días"]
       )   
       score_cot = 0
       # AUTOMOTRIZ
       if auto_cot == "Sí":
           score_cot += 3
       # CREDINISSAN (extra peso)
       if credinissan_cot == "Sí":
           score_cot += 5
       # HIPOTECARIO
       if hipotecario_cot == "Bancario":
           score_cot += 4
       elif hipotecario_cot == "Infonavit":
           score_cot += 2
       # TARJETAS
       if tarjeta_alta_cot == "Sí":
           score_cot += 4
       # ATRASOS (AQUÍ ESTÁ LA CLAVE)
       if atrasos_cot == "Sin atrasos":
           score_cot += 5
       elif atrasos_cot == "1-30 días":
           score_cot += 2
       elif atrasos_cot == "31-60 días":
           score_cot -= 4
       elif atrasos_cot == "61+ días":
           score_cot -= 10           
           
           
       if st.button("Evaluar cotitular"):

          capacidad_total = (st.session_state.ingreso + ingreso_cot) * 0.3
          if score_cot >= 12:
              buro_cot = "BUENO"
          elif score_cot >= 6:
              buro_cot = "REGULAR"
          else:
              buro_cot = "MALO"
          st.write(f"📊 Buró cotitular: {buro_cot}")
              
          if tipo_cot == "Conocido" and buro_cot != "BUENO":
           resultado_cot = "❌ Debe ser línea directa con buen historial"

          elif capacidad_total >= r["mensualidad"] and buro_cot == "BUENO":
           resultado_cot = "🟢 APROBADO FINAL"  
          elif buro_cot == "REGULAR":
              resultado_cot = "🟡 Aún condicionado (mejorar perfil)"    
          else:
            resultado_cot = "🔴 Cotitular no viable"


          st.session_state.cotitular_resultado = resultado_cot

       if st.session_state.cotitular_resultado:
           st.subheader("📊 RESULTADO FINAL")
           st.write(st.session_state.cotitular_resultado)  
   st.divider()  
   # =========================
   # 🔥 TEMPERATURA
    # =========================
   st.subheader("🔥 Temperatura de venta")
   if "CALIENTE" in r["temp"]:
           st.success(r["temp"])
   elif "TIBIO" in r["temp"]:
           st.warning(r["temp"])
   else:
           st.info(r["temp"])
    # =========================
    # 💰 APARTADO + ACCIÓN
    # =========================
   st.subheader("💰 Siguiente paso")
   if r["plan"] == "DIRECTO":
           st.success("👉 Solicitar ENGANCHE COMPLETO")
   else:
           st.warning("👉 Solicitar APARTADO $5,000")
   st.error("⚠️ Solicita anticipo para asegurar unidad")   
   st.markdown("### 🏦 Cuenta BBVA")
   st.write("Cuenta DAOSA SA DE CV: 012320001250476847")
       
       # =========================
       # 📊 COTIZADOR
       # =========================
       
   st.markdown("### 📊 Cotizador")
   st.link_button(
        "📊 Cotizar ahora",
         "https://procotiza.losnrtelepro.com.mx/Procotiza/login.aspx?mns"
       )
                      
   # =========================
   # MENSAJE PARA PDF (INTELIGENTE)
   # =========================
   mensaje_pdf = r.get("mensaje_cliente", "")    
     

   buffer = BytesIO()
   doc = SimpleDocTemplate(buffer)
   styles = getSampleStyleSheet()

   content = [

         Paragraph("SOLICITUD DE PERFILAMIENTO CREDITICIO", styles["Title"]),
         Paragraph(" ", styles["Normal"]) ,

        # DATOS CLIENTE
         Paragraph(f"<b>Cliente:</b> {r.get('nombre','')}", styles["Normal"]),
         Paragraph(f"<b>Telefono:</b> {r.get('telefono','')}", styles["Normal"]),
         Paragraph(f"<b>Correo:</b> {r.get('correo','')}", styles["Normal"]),

         Paragraph(" ", styles["Normal"]),

        # RESULTADO
         Paragraph("<b>RESULTADO DE PERFIL</b>", styles["Heading2"]),
         Paragraph(f"Estatus: {r['decision']}", styles["Normal"]),
         Paragraph(f"Probabilidad estimada: {r['prob']}%", styles["Normal"]),
         Paragraph(f"<b>Mensualidad maxima recomendada:</b> ${r.get('capacidad_pago',0):,.0f}", styles["Normal"]),

         Paragraph("<b>Resultado del análisis:</b>", styles["Heading3"]),
         Paragraph(mensaje_pdf, styles["Normal"]),
                 

         Paragraph(" ", styles["Normal"]),


        # CONDICIONES
         Paragraph("<b>Posibles validaciones durante el proceso:</b>", styles["Heading3"]),
         Paragraph("""
         - Validación de ingresos
         - Confirmación de datos                    
         - Revisión por financiera
         """, styles["Normal"]),          
 
         Paragraph(" ", styles["Normal"]),

        # CIERRE
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

        #CONTACTO
         Paragraph("<b>Contacto</b>", styles["Heading2"]),

         Paragraph(f"<b>Asesor:</b> {r.get('asesor','')}", styles["Normal"]),
         Paragraph(f"<b>Telefono:</b> {r.get('telefono_asesor','')}", styles["Normal"]),
         Paragraph(f"<b>Correo:</b> {r.get('correo_asesor','')}", styles["Normal"]),
         Paragraph(f"<b>RFC:</b> {r.get('rfc','')}", styles["Normal"]),

         Paragraph(" ", styles["Normal"]),

         Paragraph("Tu asesor está disponible para acompañarte en todo el proceso.", styles["Normal"]),

         Paragraph(" ", styles["Normal"]),

        # LEGAL
         Paragraph("<b>Nota importante:</b>", styles["Heading3"]),
         Paragraph(
            "Este documento es informativo. La aprobación final dependerá de la evaluación de la financiera conforme a buró de crédito.",
            styles["Normal"]
         ),
            ]

        # VALIDACION
       
   if not all([
         r.get("asesor", "").strip(),
         r.get("nombre", "").strip(),
         r.get("telefono", "").strip(),
          

        ]):
         st.warning("⚠️ Completa datos de cliente y asesor para generar PDF")

   else:
         doc.build(content)

         st.download_button(
            "📄 Descargar PDF",
            data=buffer.getvalue(),
            file_name="perfil.pdf",
            mime="application/pdf"

        )          
