import streamlit as st


def render_card(title, value, icon="", color="#2563EB", subtitle=""):

    st.markdown(
        f"""
        <div class="qa-card">

            <div class="qa-card-icon">
                {icon}
            </div>

            <div class="qa-card-title">
                {title}
            </div>

            <div class="qa-card-value">
                {value}
            </div>

            <div class="qa-card-subtitle">
                {subtitle}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )