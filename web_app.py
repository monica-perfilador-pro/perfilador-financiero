import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="Perfilador PRO", layout="centered")

st.markdown("""
<h1 style='text-align: center; color: #00E0FF; margin-borrom: 20px;'>
🚗 AutoScore AI
</h1>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================
if "resultado" not in st.session_state:    st.session_state.resultado = None


if "cotitular_activo" not in st.session_state:
    st.session_state.cotitular_activo = False

if "cotitular_resultado" not in st.session_state:
    st.session_state.cotitular_resultado = None

with st.form("formulario"):
  with st.container():  
    # =========================
    #  DATOS ASESOR
    # =========================
    st.markdown("# 👤 Datos del asesor")
       

    asesor = st.text_input("Nombre asesor")
    telefono_asesor = st.text_input("Teléfono asesor")
    correo_asesor = st.text_input("Correo asesor")
    rfc = st.text_input("RFC asesor")

    # =========================
    # DATOS CLIENTE
    # =========================
    st.markdown("## 👥 Datos del cliente")

    nombre_cliente = st.text_input("Nombre cliente")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo")

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
        ["Nómina", "Independiente", "No comprueba ingresos"]
    )

    negocio_casa = 2
    if tipo_ingreso == "Independiente":
        negocio_casa = st.selectbox(
            "¿Negocio en domicilio?", 
            [1,2], 
            format_func=lambda x: "Sí" if x==1 else "No"
        )    

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
      format_func=lambda x: ["Sin","Leves","Fuertes"][x-1]
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
   if hipotecario == "bancario":
        score += 2    
      
   #ATRASOS
   if atrasos == 2:          
      score -= 3
   elif atrasos == 3:     
        score -= 10
    # CONSULTAS    
   if consultas >= 8:     
       score -= 5
   elif consultas >= 5:     
      score -= 2

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

   if consultas >= 5:     
        prob -= 10

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



   # =========================     
   # VALIDACIÓN CAPACIDAD     
   # =========================     
    
   mensaje_capacidad = ""

   if excede_capacidad:     
    if prob < 70:         
      mensaje_capacidad = """⚠️ Capacidad de pago excedida.          

    ° Se recomienda ampliar plazo o reducir monto    
    ° Probable comprobacion de ingresos    
    """
      decision = "🟡 AJUSTE NECESARIO" 
      plan = "AJUSTAR_PLAZO"
   else:     
      mensaje_capacidad = """⚠️ Mensualidad alta para el ingreso.
   ° Puede requerir validacion adicional     
    """

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

   mensaje = ""
   decision = "🟡 EN EVALUACIÓN"
   plan = "REVISION"

   # 🔴 BLOQUEO TOTAL
   if atrasos == 3:
       decision = "🔴 RECHAZADO"
       plan = "KUNA"

     # 🔴 SCORE MUY BAJO
   elif score_color == "ROJO":
        decision = "🔴 RECHAZADO"
        plan = "KUNA"

        mensaje = """👉 Perfil no viable para crédito tradicional.

    Opciones:
   ° Plan KUNA (buró lastimado)
   ° Perfilar correctamente (verifica campos)
   ° Enganche alto requerido

   Recomendación:
   Ingresar con otro perfil
   """

   # ⚠️ CAPACIDAD DE PAGO (CONDICIONA)
   elif excede_capacidad and prob < 70:
        decision = "🟡 AJUSTE NECESARIO"
        plan = "AJUSTAR_PLAZO"

        mensaje = """⚠️ Capacidad de pago excedida.

   ° Ampliar plazo
   ° Reducir monto
   ° Probable validación de ingresos
   """

   # 🟠 RIESGO MEDIO (RESCATABLE)
   elif riesgo_medio and prob < 60:
        decision = "🟠 PERFIL CON RIESGO (POSIBLE RESCATE)"
        plan = "RESCATE"

        mensaje = """👉 Perfil con riesgo detectado.

   ° Subir enganche mínimo al 25%
   ° Cotitular línea directa
   ° Evitar más consultas en buró
   """

   # 🟢 PROBABILIDAD ALTA
   if prob >= 70:
      if riesgo_medio:
         decision = "🟢 APROBADO EN ANÁLISIS"
         plan = "SE VA A ANALISIS"

         mensaje = """👉 Perfil con observaciones:

   ° Posible validación de ingresos
   ° Investigación telefónica
   """
      else:
        decision = "🟢 APROBADO AUTOMÁTICO"
        plan = "DIRECTO"

   # 🟡 PERFIL MEDIO
   elif prob >= 50:
       if enganche_pct < 20 or riesgo_medio:
           decision = "🟡 APROBABLE CON CONDICIONES"
           plan = "CONDICIONADO"

           mensaje = """👉 Mejora viable:

   ° Subir enganche mínimo 10 pts     
   ° Validación de perfil por financiera     
   """ 
       else:
          decision = "🟡 PRE APROBADO"
          plan = "DIRECTO"

   # 🟡 PERFIL BAJO
   elif prob >= 35:
           decision = "🟡 RESCATABLE CON COTITULAR"
           plan = "COTITULAR"

           mensaje = """👉 Perfil bajo:

   ° Requiere cotitular con buen score
   """

   # 🔴 NO VIABLE
   else:
       decision = "🔴 RECHAZADO"
       plan = "KUNA"
    
   # INVESTIGACIÓN
   investigacion = "🟢 Sin investigación"

   if tipo_ingreso == "Independiente" and negocio_casa == 1 and prob < 80:
       investigacion = "🔴 Investigación física obligatoria"
   elif tipo_ingreso == "independiente" and prob < 70:
       investigacion = "🟡 validacion de ingresos"
   elif domicilio_buro == 2:
       investigacion = "🔴 Investigación por domicilio"
   elif tipo_ingreso != "Nómina" and prob < 45:
       investigacion = "🔴 Alta probabilidad de IF"

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
       "capacidad_pago": capacidad_pago

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
       "mensaje": mensaje,

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
       "capacidad_pago": capacidad_pago
   }

       
   st.session_state.cotitular_activo = (plan == "SIN_BURO" or plan == "COTITULAR")
   st.session_state.cotitular_resultado = None

   # =========================
   # RESULTADO
   # =========================

   if "resultado" in st.session_state:

       r = st.session_state.resultado

       st.subheader("📊 RESULTADO")

       # 🔴 SOLO mensaje condicionado
       if "mensaje" in r and r["mensaje"]:
            st.warning(r["mensaje"])

       # =========================
       # SCORE VISUAL
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
           score_label = "🔴 SCORE ROJO"
           score_desc = "Perfil de alto riesgo, probable rechazo"
    
       st.subheader(score_label)
       st.write(score_desc)
       st.write(f"Probabilidad: {r['prob']}%")
       st.markdown(f"### 💰 Tu mensualidad maxima es de: ${r[ 'capacidad_pago']:,.0f}")
       st.write(r["temp"])
       st.write(r["investigacion"])
       st.subheader(r["decision"])

       # DOCUMENTOS
       st.subheader("📄 Documentación")
       for d in r["documentos"]:
           st.write(f"• {d}")

       # =========================
       # COTITULAR
       # =========================

       if st.session_state.cotitular_activo:

           st.subheader("👥 ANALIZAR COTITULAR")

           tipo_cot = st.selectbox("Tipo cotitular", ["Línea directa","Conocido"])
           ingreso_cot = st.number_input("Ingreso cotitular")
           buro_cot = st.selectbox("Historial", ["Malo","Regular","Bueno"])

           if st.button("Evaluar cotitular"):
              capacidad_total = (ingreso + ingreso_cot) * 0.3

              if tipo_cot == "Conocido" and buro_cot != "Bueno":
                resultado_cot = "❌ Debe ser línea directa"
              elif capacidad_total >= r["mensualidad"] and buro_cot == "Bueno":
                resultado_cot = "🟢 APROBADO FINAL"
              else:
                resultado_cot = "🟡 Aún condicionado"

              st.session_state.cotitular_resultado = resultado_cot

       if st.session_state.cotitular_resultado:
          st.subheader("📊 RESULTADO FINAL")
          st.write(st.session_state.cotitular_resultado)

        # =========================
        # APARTADO
        # =========================

       st.subheader("💰 APARTADO")
       st.markdown("### 📊 Cotizador")
       st.link_button(
           "📊 Abrir Cotizador",
            "https://procotiza.losnrtelepro.com.mx/Procotiza/login.aspx?mns"
       )    

       if r["plan"] == "DIRECTO":
         st.success("👉 Solicitar ENGANCHE COMPLETO")
       else:
         st.warning("👉 Solicitar APARTADO $5,000")

         st.error("⚠️ solicita anticipo para asegurar unidad")

         st.markdown("### 🏦 Cuenta BBVA")
         st.write("Cuenta DAOSA SA DE CV: 012320001250476847")

                  
       # =========================
       # MENSAJE PARA PDF (INTELIGENTE)
       # =========================

       if r["score_color"] == "AZUL":
         mensaje_perfil = "Perfil con alta probabilidad de autorización."

         posibles_condiciones = """
         - Validación telefónica<br/>
         """
        
       elif r["score_color"] == "VERDE":
         mensaje_perfil = "Perfil sólido, sujeto a validaciones estándar."

         posibles_condiciones = """
         - Validación de ingresos<br/>
         - Validación telefónica<br/>
         """
        
       elif r["score_color"] == "AMARILLO":
         mensaje_perfil = "Perfil viable, sujeto a revisión adicional."

         posibles_condiciones = """
         - Validación de ingresos<br/>
         - Investigación telefónica o física<br/>
         - Posible ajuste de condiciones<br/>
         """

       elif r["score_color"] == "NARANJA":
         mensaje_perfil = "Perfil condicionado, requiere estructura para aprobación."

         posibles_condiciones = """
         - Cotitular recomendado<br/>
         - Investigación<br/>
         - Ajuste de enganche o plazo<br/>
         """

       else:  # ROJO
         mensaje_perfil = "Perfil de alto riesgo, se recomienda estrategia alternativa."

         posibles_condiciones = """
         - Plan alternativo (KUNA)<br/>
         - Reestructura de perfil<br/>
         - Nuevo solicitante<br/>
         """            
     

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
         Paragraph(f"Estatus: SCORE {r['score_color']}", styles["Normal"]),
         Paragraph(f"Probabilidad estimada: {r['prob']}%", styles["Normal"]),
         Paragraph(f"<b>Mensualidad maxima recomendada:</b> ${r.get('capacidad_pago',0):,.0f}", styles["Normal"]),
         Paragraph(mensaje_perfil, styles["Normal"]),
         

         Paragraph(" ", styles["Normal"]),


        # CONDICIONES
         Paragraph("<b>Posibles validaciones durante el proceso:</b>", styles["Heading3"]),
         Paragraph(f"{posibles_condiciones}", styles["Normal"]),
 
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
 
