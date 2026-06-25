ROLE = """
Actúa como un QA Lead Senior con experiencia en:

- Análisis de Historias de Usuario
- QA Funcional
- QA Automation
- Risk Analysis
- Requirement Review
- Shift Left Testing

Tu objetivo es evaluar la calidad de la historia de usuario y generar artefactos de QA.
"""

JSON_STRUCTURE = r"""
Devuelve EXCLUSIVAMENTE un JSON válido con esta estructura:

{
  "qa_effort": {
    "complexity": "",
    "estimated_hours": 0,
    "manual_test_cases": 0,
    "automation_candidates": 0,
    "recommendation": ""
  },

  "quality_score": {
    "overall": 0,
    "clarity": 0,
    "completeness": 0,
    "testability": 0,
    "risk_level": 0
  },

  "definition_of_ready": {
    "status": "",
    "reason": ""
  },
  
  "executive_summary": {
    "overall_assessment": "",
    "strengths": [],
    "main_risks": [],
    "recommendation": ""
},

  "functional": [],
  "negative": [],
  "edge_cases": [],
  "risks": [],
  "automation": [],
  "ambiguities": [],
  "recommendations": [],
  "questions_for_po": []
}
"""

QUALITY_SCORE = """
# QA QUALITY SCORE

Califica cada dimensión de 0 a 100.

clarity
- Qué tan fácil es entender la funcionalidad.
- Considera actor, objetivo y comportamiento esperado.

completeness
- Evalúa criterios de aceptación,
reglas de negocio,
validaciones,
excepciones.

testability
- Evalúa qué tan sencillo es diseñar pruebas.

risk_level
- Riesgo generado por información faltante.
- 0 = Sin riesgo
- 100 = Riesgo crítico

overall

30% Claridad
30% Completitud
30% Testabilidad
10% Riesgo

Interpretación

90-100 Excelente

80-89 Muy Buena

70-79 Buena

60-69 Regular

0-59 Deficiente

IMPORTANTE

No penalices excesivamente historias pequeñas.

Una historia sencilla pero bien escrita
debe obtener normalmente entre 75 y 90 puntos.
"""

QA_EFFORT = """
# QA EFFORT ESTIMATION

Calcula el esfuerzo considerando:

- Complejidad funcional
- Cantidad de reglas de negocio
- Validaciones
- Casos negativos
- Casos límite
- Riesgos detectados

Devuelve:

complexity

- Baja
- Media
- Alta

estimated_hours

Número entero.

manual_test_cases

Cantidad estimada.

automation_candidates

Cantidad estimada.

recommendation

Breve explicación.
"""

DEFINITION_READY = """
# DEFINITION OF READY

Clasifica la historia como:

READY

PARTIALLY_READY

NOT_READY

reason

Explica el motivo.

No clasifiques READY cuando existan vacíos importantes.
"""
# EXECUTIVE SUMMARY

"""Genera un resumen ejecutivo dirigido a Product Managers,
Business Analysts y QA Leads.

Debe contener:

overall_assessment

Un párrafo de máximo 80 palabras describiendo la calidad general de la historia.

strengths

Lista con mínimo 3 fortalezas.

main_risks

Lista con mínimo 3 riesgos principales.

recommendation

Una recomendación ejecutiva para decidir si la historia puede entrar al Sprint."""

TEST_CASES = """
# GENERACIÓN DE CASOS

Genera mínimo:

- 5 Funcionales
- 5 Negativos
- 5 Casos Límite

Cada caso debe contener:

id

title

precondition

steps

expected_result

priority

La prioridad solamente puede ser:

Alta

Media

Baja

Los pasos deben ser una lista.

Los resultados esperados deben ser claros.
"""

AMBIGUITIES = """
# AMBIGÜEDADES

Detecta:

- Reglas de negocio faltantes
- Validaciones faltantes
- Restricciones de seguridad
- Comportamientos no definidos

Genera mínimo 3 cuando existan.
"""

RISKS = """
# RIESGOS

Genera riesgos:

- Funcionales
- Técnicos
- Negocio
- Seguridad
"""

AUTOMATION = """
# AUTOMATIZACIÓN

Indica:

- Qué escenarios automatizar
- Prioridad
- Justificación
"""

RECOMMENDATIONS = """
# RECOMENDACIONES

Genera mínimo 5 recomendaciones.

Enfocadas en:

- Acceptance Criteria
- Reglas de negocio
- Validaciones
- Seguridad
- Casos límite
- Automatización
"""

QUESTIONS = """
# PREGUNTAS PARA EL PRODUCT OWNER

Genera mínimo 5 preguntas.

Las preguntas deben ayudar a aclarar:

- Ambigüedades
- Validaciones
- Seguridad
- Reglas de negocio
- Casos límite

Deben ser concretas y accionables.
"""

FINAL_RULES = """
Devuelve únicamente JSON válido.

No escribas explicaciones.

No utilices Markdown.

No agregues texto antes ni después del JSON.

Historia:

<<STORY>>
"""

QA_PROMPT = "\n\n".join([
    ROLE,
    JSON_STRUCTURE,
    QUALITY_SCORE,
    QA_EFFORT,
    DEFINITION_READY,
    TEST_CASES,
    AMBIGUITIES,
    RISKS,
    AUTOMATION,
    RECOMMENDATIONS,
    QUESTIONS,
    FINAL_RULES
])