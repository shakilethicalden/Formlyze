import json
from openpyxl import Workbook
from io import BytesIO
from collections import OrderedDict

def generate_excel(form_responses):
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Form Responses"

        all_questions = OrderedDict()

        # Collect all unique question titles
        for response in form_responses:
            try:
                for item in response.response_data:
                    if isinstance(item, str):
                        try:
                            item = json.loads(item)
                        except json.JSONDecodeError:
                            continue

                    question = item.get("question_title", "")
                    if question:
                        all_questions[question] = None
            except:
                continue

        # Set headers
        headers = ["Responder Email", "Created At"] + list(all_questions.keys())
        ws.append(headers)

        # Process each row
        for response in form_responses:
            try:
                row_data = {
                    "Responder Email": response.responder_email or "Anonymous",
                    "Created At": response.created_at.strftime("%Y-%m-%d %H:%M"),
                }

                for item in response.response_data:
                    try:
                        if isinstance(item, str):
                            item = json.loads(item)
                    except:
                        continue

                    field_type = item.get("field_type", "")
                    question = item.get("question_title", "")
                    answer = item.get("response", "")

                    if not question:
                        continue

                    try:
                        if field_type == "address" and isinstance(answer, dict):
                            full_address = ", ".join([str(v) for v in answer.values() if v])
                            row_data[question] = full_address
                        elif field_type == "checkbox" and isinstance(answer, list):
                            row_data[question] = ", ".join(answer)
                        elif field_type in ["file", "signature"]:
                            row_data[question] = answer or "No file"
                        else:
                            row_data[question] = answer
                    except:
                        row_data[question] = "Error"

                row = [row_data.get(col, "") for col in headers]
                ws.append(row)

            except:
                continue

        # Create Excel in memory
        virtual_workbook = BytesIO()
        wb.save(virtual_workbook)
        virtual_workbook.seek(0)
        virtual_workbook.name = "form_responses.xlsx"  # ensure compatibility with FileResponse
        return virtual_workbook

    except:
        return None  
