import streamlit as st


def metric_card(icon, title, value, subtitle="", color="#3B82F6"):

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-icon"
                 style="background:{color};">
                {icon}
            </div>

            <div class="metric-title">
                {title}
            </div>

            <div class="metric-value">
                {value}
            </div>

            <div class="metric-subtitle">
                {subtitle}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )