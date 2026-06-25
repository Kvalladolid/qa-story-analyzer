import streamlit as st
from pathlib import Path

from services.ai_service import analyze_story
from services.excel_service import generate_excel

from ui.header import render_header
from ui.form import render_form
from ui.dashboard import render_dashboard
from ui.tabs import render_tabs
from ui.download import render_download
from ui.executive_summary import render_executive_summary


# =========================
# CONFIGURACIÓN
# =========================

st.set_page_config(
    page_title="QA Story Analyzer",
    page_icon="🧪",
    layout="wide"
)


# =========================
# CSS
# =========================

def load_css():
    css_file = Path("styles/main.css")

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# =========================
# HEADER
# =========================

render_header()


# =========================
# FORMULARIO
# =========================

story, analyze = render_form()


# =========================
# ANALYSIS
# =========================

if analyze:

    if not story.strip():

        st.warning("Ingresa una historia de usuario.")
        st.stop()

    with st.spinner("🤖 Analizando historia..."):

        result = analyze_story(story)

    render_dashboard(result)
    
    render_tabs(result)
    render_executive_summary(result)

    excel_file = generate_excel(result)

    render_download(excel_file)