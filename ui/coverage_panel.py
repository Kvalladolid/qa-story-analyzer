import streamlit as st


def render_coverage_panel(result):

    total_tests = (
        len(result["functional"])
        + len(result["negative"])
        + len(result["edge_cases"])
    )

    coverage = min((total_tests / 15) * 100, 100)

    st.subheader("📈 QA Coverage")

    st.progress(coverage / 100)

    st.caption(
        f"QA Coverage Score: {coverage:.0f}%"
    )