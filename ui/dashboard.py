import streamlit as st

from ui.requirements_panel import render_requirements_panel
from ui.executive_summary import render_executive_summary
from ui.quality_details import render_quality_details
from ui.coverage_panel import render_coverage_panel


def render_dashboard(result):
    """
    Dashboard principal del análisis QA.
    Solo orquesta los componentes de la interfaz.
    """

    # ==========================================================
    # REQUIREMENTS INTELLIGENCE
    # ==========================================================

    render_requirements_panel(result)

    st.markdown("---")

    # ==========================================================
    # AI EXECUTIVE SUMMARY
    # ==========================================================

    render_executive_summary(result)

    st.markdown("---")

    # ==========================================================
    # QUALITY DETAILS
    # ==========================================================

    render_quality_details(result)

    st.markdown("---")

    # ==========================================================
    # COVERAGE
    # ==========================================================

    render_coverage_panel(result)

    st.markdown("---")