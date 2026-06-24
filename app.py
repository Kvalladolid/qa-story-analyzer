import streamlit as st
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO
from openpyxl import Workbook


from pathlib import Path

def load_css():
    css_file = Path("styles/main.css")

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()
# =========================
# CONFIGURACIÓN
# =========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

st.set_page_config(
    page_title="QA Story Analyzer",
    page_icon="🧪",
    layout="wide"
)

# =========================
# OPENAI ANALYSIS
# =========================

def analyze_story(story):

 prompt = f"""
 Actúa como un QA Lead Senior con experiencia en:

- Análisis de Historias de Usuario
- QA Funcional
- QA Automation
- Risk Analysis
- Requirement Review
- Shift Left Testing

 Tu objetivo es evaluar la calidad de la historia de usuario y generar artefactos de QA.

 Devuelve EXCLUSIVAMENTE un JSON válido con esta estructura:

{{
  "qa_effort": {{
    "complexity": "",
    "estimated_hours": 0,
    "manual_test_cases": 0,
    "automation_candidates": 0,
    "recommendation": ""
  }},

  "quality_score": {{
    "overall": 0,
    "clarity": 0,
    "completeness": 0,
    "testability": 0,
    "risk_level": 0
  }},

  "definition_of_ready": {{
    "status": "",
    "reason": ""
  }},

  "functional": [],
  "negative": [],
  "edge_cases": [],
  "risks": [],
  "automation": [],
  "ambiguities": [],
  "recommendations": [],
  "questions_for_po": []
}}

REGLAS PARA EL QA QUALITY SCORE

Califica cada dimensión de 0 a 100.

clarity:
- Qué tan fácil es entender la funcionalidad.
- Debe considerar objetivo, actor y comportamiento esperado.

completeness:
- Qué tan completos son los criterios de aceptación.
- Considera reglas de negocio, validaciones y excepciones.

testability:
- Qué tan fácil es diseñar y ejecutar pruebas.
- Considera si existen criterios verificables.

risk_level:
- Riesgo generado por información faltante.
- 0 = Sin riesgo.
- 100 = Riesgo crítico.

overall:
- Promedio ponderado:
  30% claridad
  30% completitud
  30% testabilidad
  10% riesgo
  
QA Estimation
Calcula el esfuerzo de QA considerando:
- Cantidad de reglas de negocio.
- Complejidad funcional.
- Cantidad de validaciones.
- Casos negativos requeridos.
- Casos límite requeridos.
- Riesgos identificados.
Devuelve:
complexity:
- Baja
- Media
- Alta
estimated_hours:
- Número estimado de horas QA.
manual_test_cases:
- Cantidad estimada de casos manuales.
automation_candidates:
- Cantidad estimada de casos automatizables.
recommendation:
- Explicación breve del esfuerzo.

Genera preguntas para el Product Owner o Business Analyst.

Las preguntas deben:

- Resolver ambigüedades detectadas.
- Aclarar reglas de negocio faltantes.
- Aclarar validaciones no definidas.
- Aclarar restricciones de seguridad.
- Ser concretas y accionables.
- Generar mínimo 5 preguntas.

INTERPRETACIÓN

90-100 = Excelente
80-89 = Muy buena
70-79 = Buena
60-69 = Regular
0-59 = Deficiente

Definition of Ready:

- READY: La historia tiene suficiente detalle para iniciar desarrollo.
- PARTIALLY_READY: La historia requiere algunas aclaraciones menores.
- NOT_READY: La historia tiene vacíos importantes que impiden iniciar desarrollo.

Para definition_of_ready devuelve:

status:
- READY
- PARTIALLY_READY
- NOT_READY

reason:
- Explica brevemente por qué recibió esa clasificación.

IMPORTANTE:

NO penalices excesivamente historias pequeñas.

Ejemplo:

Historia:
"Como usuario quiero recuperar mi contraseña para acceder nuevamente al sistema."

Criterios:
- Email válido
- Link válido 24 horas
- Contraseña mínima 12 caracteres

Esta historia normalmente debería obtener:

clarity: 85-95
completeness: 70-85
testability: 80-95
risk_level: 20-40
overall: 75-90

Generación de Casos:

Genera mínimo:

- 5 funcionales
- 5 negativos
- 5 casos límite

Cada caso debe contener:

{{
  "id": "",
  "title": "",
  "precondition": "",
  "steps": [],
  "expected_result": "",
  "priority": ""
}}

La prioridad solo puede ser:

- Alta
- Media
- Baja

Ambigüedades:

Identifica:

- Reglas de negocio faltantes
- Validaciones faltantes
- Restricciones de seguridad faltantes
- Comportamientos no definidos

Genera mínimo 3 cuando existan.

Recommendations:

Genera recomendaciones concretas para mejorar la calidad de la Historia de Usuario.

Las recomendaciones deben enfocarse en:

- Criterios de aceptación faltantes.
- Reglas de negocio no definidas.
- Validaciones faltantes.
- Seguridad.
- Casos límite no contemplados.
- Consideraciones para QA y automatización.

Genera mínimo 5 recomendaciones accionables.

Ejemplos:

- Definir comportamiento para correos no registrados.
- Especificar si el link puede reutilizarse.
- Agregar límite de intentos de recuperación.
- Definir complejidad mínima de contraseña.
- Especificar comportamiento ante expiración del link.

Riesgos:

Genera riesgos:

- Funcionales
- Técnicos
- Negocio
- Seguridad

Automatización:

Indica qué pruebas deberían automatizarse y por qué.

Recommendations:

Genera recomendaciones para mejorar la historia de usuario.

Ejemplos:

- Agregar criterios de aceptación para correos inexistentes.
- Definir comportamiento de links expirados.
- Especificar política de complejidad de contraseña.
- Definir límites de intentos.

Devuelve únicamente JSON válido.
No incluyas texto fuera del JSON.
Historia:

{story}
"""

 response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

 return json.loads(
        response.choices[0].message.content
    )
# =========================
# EXCEL EXPORT
# =========================

def generate_excel(result):

    wb = Workbook()

    ws = wb.active
    ws.title = "QA Analysis"

    ws.append([
        "ID",
        "Tipo",
        "Prioridad",
        "Título",
        "Precondición",
        "Pasos",
        "Resultado Esperado"
    ])

    for tc in result["functional"]:

        ws.append([
            tc["id"],
            "Funcional",
            tc["priority"],
            tc["title"],
            tc["precondition"],
            "\n".join(tc["steps"]),
            tc["expected_result"]
        ])

    for tc in result["negative"]:

        ws.append([
            tc["id"],
            "Negativo",
            tc["priority"],
            tc["title"],
            tc["precondition"],
            "\n".join(tc["steps"]),
            tc["expected_result"]
        ])

    for tc in result["edge_cases"]:

        ws.append([
            tc["id"],
            "Caso Límite",
            tc["priority"],
            tc["title"],
            tc["precondition"],
            "\n".join(tc["steps"]),
            tc["expected_result"]
        ])

    buffer = BytesIO()

    wb.save(buffer)

    buffer.seek(0)

    return buffer

# =========================
# UI
# =========================

st.title("🧪 QA Story Analyzer")
st.caption(
    "AI-Powered Requirements Intelligence"
)

st.markdown(
    """
     Analiza historias de usuario, detecta ambigüedades,
    evalúa su calidad y determina si están listas para desarrollo.
    """
)
st.markdown("""

""", unsafe_allow_html=True)
st.markdown("---")

story = st.text_area(
    "Pega tu User Story",
    height=180,
    placeholder="""
Como usuario quiero recuperar mi contraseña
para poder acceder nuevamente al sistema.

Criterios de aceptación:
- Email válido
- Link válido por 24 horas
- Contraseña mínima 12 caracteres
"""
)

analyze = st.button(
    "🚀 Analizar Historia",
    use_container_width=True
)

# =========================
# ANALYSIS
# =========================

if analyze:

    if not story:
        st.warning("Ingresa una historia de usuario")
        st.stop()

    with st.spinner("Analizando historia..."):

        result = analyze_story(story)
        score = result["quality_score"]
        dor = result["definition_of_ready"]

    st.markdown("---")

    st.subheader("📊 QA Quality Score")

    s1, s2, s3, s4, s5 = st.columns(5)

    s1.metric("🎯 General", f"{score['overall']}/100")
    s2.metric("📝 Claridad", score["clarity"])
    s3.metric("📋 Completitud", score["completeness"])
    s4.metric("🧪 Testabilidad", score["testability"])
    s5.metric("⚠️ Riesgo", score["risk_level"])

    st.subheader("🚦 Definition of Ready")

    if dor["status"] == "READY":
      st.success(
        f"✅ {dor['status']} - {dor['reason']}"
    )

    elif dor["status"] == "PARTIALLY_READY":
      st.warning(
        f"⚠️ {dor['status']} - {dor['reason']}"
    )

    else:
     st.error(
        f"❌ {dor['status']} - {dor['reason']}"
    )

    st.markdown("---")
    st.subheader("📑 Executive Summary")

    st.info(
    f"""
   • Score General: {score['overall']}/100

   • Definition of Ready: {dor['status']}

   • Casos generados:
    {len(result['functional'])} funcionales,
    {len(result['negative'])} negativos,
    {len(result['edge_cases'])} límite

   • Riesgos identificados:
    {len(result['risks'])}

   • Ambigüedades detectadas:
    {len(result['ambiguities'])}

   • Preguntas para refinamiento:
    {len(result['questions_for_po'])}
    """
)

    effort = result["qa_effort"]
    st.markdown("---")

    st.subheader("⏱️ QA Estimation")

    e1, e2, e3, e4 = st.columns(4)

    e1.metric(
    "Complejidad",
    effort["complexity"]
)

    e2.metric(
    "Horas QA",
    effort["estimated_hours"]
)

    e3.metric(
    "Casos Manuales",
    effort["manual_test_cases"]
)

    e4.metric(
    "Automatizables",
    effort["automation_candidates"]
)

    st.info(
    effort["recommendation"]
)

    st.markdown("---")

    # KPIs

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "📋 Funcionales",
        len(result["functional"])
    )

    col2.metric(
        "❌ Negativos",
        len(result["negative"])
    )

    col3.metric(
        "🧪 Casos Límite",
        len(result["edge_cases"])
    )

    col4.metric(
        "⚠️ Riesgos",
        len(result["risks"])
    )

    col5.metric(
        "🤖 Automatización",
        len(result["automation"])
    )

    # Coverage Score

    total_tests = (
        len(result["functional"])
        + len(result["negative"])
        + len(result["edge_cases"])
    )

    coverage = min(
    (total_tests / 15) * 100,
    100
)

    st.progress(
    coverage / 100
)

    st.caption(
    f"QA Coverage Score: {coverage:.0f}%"
)
    # Resultado

    st.subheader("📋 Resultado del Análisis")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📋 Funcionales",
    "❌ Negativos",
    "🧪 Casos Límite",
    "⚠️ Riesgos",
    "🤖 Automatización",
    "❓ Ambigüedades",
    "💡 Mejoras",
    "Questions for Product Team"
])

    with tab1:
       for tc in result["functional"]:

        with st.expander(
            f"{tc['id']} - {tc['title']}"
        ):


         st.write(f"**Prioridad:** {tc['priority']}")
         st.write(f"**Precondición:** {tc['precondition']}")

         st.write("**Pasos:**")

         for step in tc["steps"]:
                st.write(f"- {step}")

        st.write(
                f"**Resultado esperado:** {tc['expected_result']}"
            )

    with tab2:

     for tc in result["negative"]:

        with st.expander(
            f"{tc['id']} - {tc['title']}"
        ):

            st.write(f"**Prioridad:** {tc['priority']}")
            st.write(f"**Precondición:** {tc['precondition']}")

            st.write("**Pasos:**")

            for step in tc["steps"]:
                st.write(f"- {step}")

            st.write(
                f"**Resultado esperado:** {tc['expected_result']}"
            )

    with tab3:

      for tc in result["edge_cases"]:

        with st.expander(
            f"{tc['id']} - {tc['title']}"
        ):

            st.write(f"**Prioridad:** {tc['priority']}")
            st.write(f"**Precondición:** {tc['precondition']}")

            st.write("**Pasos:**")

            for step in tc["steps"]:
                st.write(f"- {step}")

            st.write(
                f"**Resultado esperado:** {tc['expected_result']}"
            )

    with tab4:
        for item in result["risks"]:
            st.warning(item)

    with tab5:
        for item in result["automation"]:
            st.write("•", item)
    with tab6:

      for item in result["ambiguities"]:
        st.warning(item)
        
    with tab7:
      st.subheader("💡 Recomendaciones para mejorar la Historia")
      for item in result["recommendations"]:
        st.success(item)
        
    with tab8:
      st.subheader("🎯 Preguntas para Refinamiento")
      for item in result["questions_for_po"]:
        st.info(item)

    # Excel

    excel_file = generate_excel(result)

    st.download_button(
        label="📥 Descargar Excel",
        data=excel_file,
        file_name="qa_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )