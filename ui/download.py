import streamlit as st


def render_download(excel_file):

    st.download_button(
        label="📥 Descargar Excel",
        data=excel_file,
        file_name="qa_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )