import streamlit as st


def render_test_cases(test_cases):
    """
    Renderiza cualquier lista de casos de prueba.
    """

    for tc in test_cases:

        with st.expander(f"{tc['id']} - {tc['title']}"):

            st.write(f"**Prioridad:** {tc['priority']}")
            st.write(f"**Precondición:** {tc['precondition']}")

            st.write("**Pasos:**")

            for step in tc["steps"]:
                st.write(f"- {step}")

            st.write(
                f"**Resultado esperado:** {tc['expected_result']}"
            )


def render_tabs(result):

    st.subheader("📋 Resultado del Análisis")

    (
        tab1,
        tab2,
        tab3,
        tab4,
        tab5,
        tab6,
        tab7,
        tab8
    ) = st.tabs([
        "📋 Funcionales",
        "❌ Negativos",
        "🧪 Casos Límite",
        "⚠️ Riesgos",
        "🤖 Automatización",
        "❓ Ambigüedades",
        "💡 Mejoras",
        "🎯 Preguntas PM"
    ])

    # ===========================
    # Funcionales
    # ===========================

    with tab1:
        render_test_cases(
            result["functional"]
        )

    # ===========================
    # Negativos
    # ===========================

    with tab2:
        render_test_cases(
            result["negative"]
        )

    # ===========================
    # Casos límite
    # ===========================

    with tab3:
        render_test_cases(
            result["edge_cases"]
        )

    # ===========================
    # Riesgos
    # ===========================

    with tab4:

        if result["risks"]:

            for risk in result["risks"]:
                st.warning(risk)

        else:
            st.success("No se identificaron riesgos.")

    # ===========================
    # Automatización
    # ===========================

    with tab5:

        if result["automation"]:

            for item in result["automation"]:
                st.info(item)

        else:
            st.success("No existen recomendaciones de automatización.")

    # ===========================
    # Ambigüedades
    # ===========================

    with tab6:

        if result["ambiguities"]:

            for item in result["ambiguities"]:
                st.warning(item)

        else:
            st.success("No se detectaron ambigüedades.")

    # ===========================
    # Mejoras
    # ===========================

    with tab7:

        st.subheader("💡 Recomendaciones")

        if result["recommendations"]:

            for item in result["recommendations"]:
                st.success(item)

        else:
            st.success("No existen recomendaciones.")

    # ===========================
    # Preguntas para PO
    # ===========================

    with tab8:

        st.subheader("🎯 Preguntas para Refinamiento")

        if result["questions_for_po"]:

            for item in result["questions_for_po"]:
                st.info(item)

        else:
            st.success("No existen preguntas para el Product Owner.")