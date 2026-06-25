import streamlit as st

from ui.cards import render_card


def render_requirements_panel(result):

    score = result["quality_score"]
    dor = result["definition_of_ready"]
    effort = result["qa_effort"]

    total_tests = (
        len(result["functional"])
        + len(result["negative"])
        + len(result["edge_cases"])
    )

    coverage = min((total_tests / 15) * 100, 100)

    st.subheader("🧠 Requirements Intelligence")

    row1 = st.columns(4)

    with row1[0]:
        render_card(
            title="QA Score",
            value=f"{score['overall']}/100",
            icon="🎯",
            subtitle="Overall Quality"
        )

    with row1[1]:
        render_card(
            title="Definition Ready",
            value=dor["status"],
            icon="🚦",
            subtitle="Development Readiness"
        )

    with row1[2]:
        render_card(
            title="QA Effort",
            value=f"{effort['estimated_hours']} h",
            icon="⏱",
            subtitle=effort["complexity"]
        )

    with row1[3]:
        render_card(
            title="Coverage",
            value=f"{coverage:.0f}%",
            icon="📈",
            subtitle="Test Coverage"
        )

    row2 = st.columns(4)

    with row2[0]:
        render_card(
            title="Risks",
            value=len(result["risks"]),
            icon="⚠️",
            subtitle="Detected Risks"
        )

    with row2[1]:
        render_card(
            title="Ambiguities",
            value=len(result["ambiguities"]),
            icon="❓",
            subtitle="Requirements Gaps"
        )

    with row2[2]:
        render_card(
            title="Questions",
            value=len(result["questions_for_po"]),
            icon="💬",
            subtitle="For Product Team"
        )

    with row2[3]:
        render_card(
            title="Automation",
            value=len(result["automation"]),
            icon="🤖",
            subtitle="Automation Candidates"
        )