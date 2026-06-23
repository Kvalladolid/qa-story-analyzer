import streamlit as st
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO
from openpyxl import Workbook



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
Actúa como un QA Lead Senior con experiencia en testing funcional, automatización y análisis de riesgos.

Analiza la siguiente historia de usuario.

Genera casos de prueba completos.

Devuelve EXCLUSIVAMENTE un JSON válido con esta estructura:

{{
  "functional": [
    {{
      "id": "",
      "title": "",
      "precondition": "",
      "steps": [],
      "expected_result": "",
      "priority": ""
    }}
  ],
  "negative": [
    {{
      "id": "",
      "title": "",
      "precondition": "",
      "steps": [],
      "expected_result": "",
      "priority": ""
    }}
  ],
  "edge_cases": [
    {{
      "id": "",
      "title": "",
      "precondition": "",
      "steps": [],
      "expected_result": "",
      "priority": ""
    }}
  ],
  "risks": [],
  "automation": []
}}

Reglas:

- Genera mínimo 5 casos funcionales.
- Genera mínimo 5 negativos.
- Genera mínimo 5 casos límite.
- La prioridad debe ser Alta, Media o Baja.
- Los pasos deben venir como lista.
- El resultado esperado debe ser detallado.
- Devuelve únicamente JSON.

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

    ws.append(["Categoria", "Detalle"])

    for item in result["functional"]:
        ws.append(["Funcional", item])

    for item in result["negative"]:
        ws.append(["Negativo", item])

    for item in result["edge_cases"]:
        ws.append(["Caso Limite", item])

    for item in result["risks"]:
        ws.append(["Riesgo", item])

    for item in result["automation"]:
        ws.append(["Automatizacion", item])

    buffer = BytesIO()

    wb.save(buffer)

    buffer.seek(0)

    return buffer

# =========================
# UI
# =========================

st.title("🧪 QA Story Analyzer")

st.caption(
    "Analiza historias de usuario, identifica riesgos y genera escenarios de prueba con IA"
)

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

    st.progress(min(total_tests / 20, 1.0))

    st.caption(
        f"QA Coverage Score: {total_tests} escenarios identificados"
    )

    # Resultado

    st.subheader("📋 Resultado del Análisis")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Funcionales",
        "❌ Negativos",
        "🧪 Casos Límite",
        "⚠️ Riesgos",
        "🤖 Automatización"
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
        for item in result["negative"]:
            st.error(item)

    with tab3:
        for item in result["edge_cases"]:
            st.info(item)

    with tab4:
        for item in result["risks"]:
            st.warning(item)

    with tab5:
        for item in result["automation"]:
            st.write("•", item)

    # Excel

    excel_file = generate_excel(result)

    st.download_button(
        label="📥 Descargar Excel",
        data=excel_file,
        file_name="qa_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )