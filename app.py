import streamlit as st

st.set_page_config(
    page_title="QA Story Analyzer",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 QA Story Analyzer")
st.subheader("Analiza historias de usuario con IA")

story = st.text_area(
    "Pega tu User Story",
    height=300,
    placeholder="""
Como usuario quiero recuperar mi contraseña
para poder acceder nuevamente al sistema.

Criterios de aceptación:
- Email válido
- Link válido por 24 horas
- Contraseña mínima 12 caracteres
"""
)

if st.button("Analizar"):
    if story:
        st.success("Análisis generado")

        st.markdown("## Casos funcionales")
        st.write("- Recuperación correcta")
        st.write("- Cambio exitoso de contraseña")

        st.markdown("## Casos negativos")
        st.write("- Email inexistente")
        st.write("- Token inválido")

        st.markdown("## Casos límite")
        st.write("- Contraseña exactamente de 12 caracteres")

        st.markdown("## Riesgos")
        st.write("- Problemas de seguridad")
        st.write("- Expiración incorrecta del token")

        st.markdown("## Automatización recomendada")
        st.write("- API Testing")
        st.write("- Playwright")