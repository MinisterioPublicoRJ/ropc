from openpyxl import Workbook
from io import BytesIO

def gera_planilha_excel(rows, header, sheet_title):
    workbook = Workbook()
    sheet = workbook[workbook.sheetnames[0]]
    sheet.title = sheet_title
    # Escreve cabeçalho
    sheet.append(header)
    for row in rows:
        sheet.append(row)

    buffer_ = BytesIO()
    workbook.save(buffer_)
    buffer_.seek(0)
    return buffer_