from io import BytesIO
from openpyxl import Workbook


def generate_excel(result):

    wb = Workbook()

    ws = wb.active
    ws.title = "QA Analysis"

    ws.append([
        "ID",
        "Tipo",
        "Prioridad",
        "Título",
        "Precondición",
        "Pasos",
        "Resultado Esperado"
    ])

    sections = [
        ("functional", "Funcional"),
        ("negative", "Negativo"),
        ("edge_cases", "Caso Límite")
    ]

    for key, tipo in sections:

        for tc in result.get(key, []):

            ws.append([
                tc.get("id", ""),
                tipo,
                tc.get("priority", ""),
                tc.get("title", ""),
                tc.get("precondition", ""),
                "\n".join(tc.get("steps", [])),
                tc.get("expected_result", "")
            ])

    buffer = BytesIO()

    wb.save(buffer)

    buffer.seek(0)

    return buffer