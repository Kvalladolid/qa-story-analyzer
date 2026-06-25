import streamlit as st


def render_executive_summary(result):

    summary = result["executive_summary"]

    st.subheader("🧠 AI Executive Summary")

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown("### Overall Assessment")

        st.info(
            summary["overall_assessment"]
        )

        st.markdown("### 🚀 Recommendation")

        st.success(
            summary["recommendation"]
        )

    with col2:

        st.markdown("### ✅ Strengths")

        for item in summary["strengths"]:
            st.write(f"✔ {item}")

        st.markdown("### ⚠ Main Risks")

        for item in summary["main_risks"]:
            st.write(f"• {item}")

    st.markdown("---")