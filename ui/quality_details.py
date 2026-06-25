import streamlit as st


def render_quality_details(result):

    score = result["quality_score"]

    st.subheader("📊 Quality Details")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📝 Claridad",
            f"{score['clarity']}/100"
        )

    with col2:
        st.metric(
            "📋 Completitud",
            f"{score['completeness']}/100"
        )

    with col3:
        st.metric(
            "🧪 Testabilidad",
            f"{score['testability']}/100"
        )

    with col4:
        st.metric(
            "⚠️ Riesgo",
            f"{score['risk_level']}/100"
        )