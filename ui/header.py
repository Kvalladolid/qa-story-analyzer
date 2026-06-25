import streamlit as st


def render_header():

    st.title("🧪 QA Story Analyzer")

    st.caption(
        "AI-Powered Requirements Intelligence"
    )

    st.markdown("""
Analiza historias de usuario, detecta ambigüedades,
evalúa su calidad y determina si están listas para desarrollo.
""")

    st.markdown("---")