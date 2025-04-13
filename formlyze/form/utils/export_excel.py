import json
from openpyxl import Workbook
from io import BytesIO
from collections import OrderedDict

def generate_excel(form_responses):
    wb = Workbook()
    ws = wb.active
    ws.title = "Form Responses"

    all_questions = OrderedDict()

  
    for response in form_responses:
        for item in response.response_data:
            if isinstance(item, str):
                try:
                    item = json.loads(item)
                except json.JSONDecodeError:
                    continue
            question = item.get("question_title", "")
            if question:
                all_questions[question] = None

    headers = ["Responder Email", "Created At"] + list(all_questions.keys())
    ws.append(headers)


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
            question = item.get("question_title", "")
            answer = item.get("response", "")
            if question:
                row_data[question] = answer

      
        row = [row_data.get(col, "") for col in headers]
        ws.append(row)

    virtual_workbook = BytesIO()
    wb.save(virtual_workbook)
    virtual_workbook.seek(0)
    return virtual_workbook
