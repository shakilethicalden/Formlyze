import json
from openpyxl import Workbook
from io import BytesIO
from collections import OrderedDict

def generate_excel(form_responses):
    wb = Workbook()
    ws = wb.active
    ws.title = "Form Responses"

    all_questions = OrderedDict()

# get all questions
    for response in form_responses:
        for item in response.response_data:
            if isinstance(item, str):
                try:
                    item = json.loads(item)
                except json.JSONDecodeError:
                    continue

            question = item.get("question_title", "")
            all_questions[question] = None

  #header
    headers = ["Responder Email", "Created At"] + list(all_questions.keys())
    ws.append(headers)
# rows
    for response in form_responses:
        row_data = {
            "Responder Email": response.responder_email or "Anonymous",
            "Created At": response.created_at.strftime("%Y-%m-%d %H:%M"),
        }

        for item in response.response_data:
            if isinstance(item, str):
                try:
                    item = json.loads(item)
                except json.JSONDecodeError:
                    continue

            field_type = item.get("field_type", "")
            question = item.get("question_title", "")
            answer = item.get("response", "")

            if field_type == "address" and isinstance(answer, dict):
                full_address = ", ".join(
                    [str(v) for v in answer.values() if v]
                )
                row_data[question] = full_address
            elif field_type == "checkbox" and isinstance(answer, list):
                row_data[question] = ", ".join(answer)
            elif field_type in ["file", "signature"]:
                row_data[question] = answer or "No file"
            else:
                row_data[question] = answer

        row = [row_data.get(col, "") for col in headers]
        ws.append(row)

    # Return Excel file as bytes
    virtual_workbook = BytesIO()
    wb.save(virtual_workbook)
    virtual_workbook.seek(0)
    return virtual_workbook
