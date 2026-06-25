import streamlit as st


def render_form():

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

    return story, analyze