import os
from uuid import UUID
from django.conf import settings
from datetime import date, datetime, time
from io import BytesIO
from openpyxl import Workbook
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from operations.models import Operacao

# Constantes de layout
FOOTER_HEIGHT = 35
LINE_HEIGHT = 12
SECTION_SPACING = 12
HEADER_HEIGHT = 84

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


def date_or_time_formatter(data):
    if isinstance(data, datetime):
        return data.strftime("%d/%m/%Y %H:%M")
    elif isinstance(data, date):
        return data.strftime("%d/%m/%Y")
    elif isinstance(data, time):
        return data.strftime("%H:%M")
    return data


def format_value_for_display(value):
    if value is None or str(value).strip() == "":
        return "não preenchido"
    if isinstance(value, bool):
        return "sim" if value else "não"
    if value == "Pr":
        return "programada"
    if value == "Em":
        return "emergencial"
    if isinstance(value, (date, datetime)):
        return date_or_time_formatter(value)
    return str(value)


def break_text(text, max_width, font_size=12, is_bold=False):
    text = str(text)
    font = "Helvetica-Bold" if is_bold else "Helvetica"
    words = text.split()
    lines, current_line, current_width = [], [], 0

    for word in words:
        word_width = stringWidth(word + ' ', font, font_size)

        if stringWidth(word, font, font_size) > max_width:
            for char in word:
                char_width = stringWidth(char, font, font_size)
                if current_width + char_width <= max_width:
                    current_line.append(char)
                    current_width += char_width
                else:
                    lines.append(''.join(current_line))
                    current_line, current_width = [char], char_width
            if current_line:
                lines.append(''.join(current_line))
                current_line, current_width = [], 0
        elif current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width
        else:
            lines.append(' '.join(current_line))
            current_line, current_width = [word], word_width

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def set_style(p, font="Helvetica", size=12, color="#505050"):
    p.setFont(font, size)
    p.setFillColor(HexColor(color))


def include_header(p, width):
    img_header = os.path.join(settings.BASE_DIR, "static", "img", "bg-inicial-page.png")
    p.drawImage(img_header, 0, height_total - HEADER_HEIGHT, width=width, height=HEADER_HEIGHT)

    set_style(p, size=12, color="#353535")
    emitido_em = f"Emitido em: {date_or_time_formatter(datetime.now())}"
    y = height_total - HEADER_HEIGHT - 11 - 12
    p.drawString(width - stringWidth(emitido_em, "Helvetica", 12) - 30, y, emitido_em)

    return y - 32


def include_footer(p, width, page_number):
    p.setStrokeColor(HexColor("#F7CF32"))
    p.setLineWidth(10)
    p.line(0, 0, width, 0)
    set_style(p, size=10)
    pg_text = f"Página {page_number}"
    p.drawString(width - stringWidth(pg_text, "Helvetica", 10) - 30, 15, pg_text)


def ensure_space(p, required_height, footer_height, page_number, font="Helvetica", font_size=12, color="#505050"):
    global available_height
    if available_height < footer_height + required_height:
        include_footer(p, width_total, page_number)
        p.showPage()
        page_number += 1
        available_height = include_header(p, width_total)
        set_style(p, font, font_size, color)
    return page_number


def load_query(where_condition=None):
    query_path = os.path.join(settings.BASE_DIR, 'query', 'query.sql')
    with open(query_path, 'r', encoding='utf-8') as file:
        query_sql = file.read()
    return query_sql.replace('/* WHERE_CONDITION */', f'WHERE {where_condition}' if where_condition else '')


def draw_first_page_content(p, margin_left, operation_name, content_width, footer_height, page_number):
    global available_height

    set_style(p, "Helvetica-Bold", 14)
    p.drawString(margin_left, available_height, "Visualizar operação")
    available_height -= 26

    set_style(p, "Helvetica-Bold", 10, "#9F9F9F")
    for line in break_text(operation_name, content_width, font_size=10, is_bold=True):
        if available_height < footer_height + 10:
            include_footer(p, width_total, page_number)
            p.showPage()
            page_number += 1
            available_height = include_header(p, width_total)
            set_style(p, "Helvetica-Bold", 10, "#9F9F9F")
        p.drawString(margin_left, available_height, line)
        available_height -= 10

    p.setStrokeColor(HexColor("#F7CF32"))
    p.setLineWidth(1)
    p.line(margin_left, available_height - 5, margin_left + content_width, available_height - 5)
    available_height -= 30

    return page_number


def draw_operation_details(attributes, page_number, footer_height, p, content_width, margin_left):
    global available_height

    ignored_keys = {"id", "Criado em", "Seção Atual", "Dado registrado fora do sistema", "Cadastro Completo", "Nome da operação"}
    special_keys = {
        "Justificativa da excepcionalidade da operação",
        "Objetivo estratégico da operação",
        "Análise de riscos e medidas de controle"
    }

    for key, value in attributes.items():
        if key in ignored_keys:
            continue

        shown_value = format_value_for_display(value)

        if key in special_keys:
            set_style(p, "Helvetica-Bold", 12)
            for line in break_text(f"{key}:", content_width, is_bold=True):
                page_number = ensure_space(p, LINE_HEIGHT, footer_height, page_number)
                p.drawString(margin_left, available_height, line)
                available_height -= LINE_HEIGHT

            set_style(p, "Helvetica", 12)
            for line in break_text(shown_value, content_width):
                page_number = ensure_space(p, LINE_HEIGHT, footer_height, page_number)
                p.drawString(margin_left, available_height, line)
                available_height -= LINE_HEIGHT
        else:
            key_text = f"{key}: "
            key_width = stringWidth(key_text, "Helvetica-Bold", 12)

            page_number = ensure_space(p, LINE_HEIGHT, footer_height, page_number, font="Helvetica-Bold", font_size=12)
            set_style(p, "Helvetica-Bold", 12)
            p.drawString(margin_left, available_height, key_text)

            value_lines = break_text(shown_value, content_width - key_width)
            if value_lines:
                set_style(p, "Helvetica", 12)
                page_number = ensure_space(p, LINE_HEIGHT, footer_height, page_number, "Helvetica", 12)
                p.drawString(margin_left + key_width, available_height, value_lines[0])

                for line in value_lines[1:]:
                    available_height -= LINE_HEIGHT
                    page_number = ensure_space(p, LINE_HEIGHT, footer_height, page_number)
                    p.drawString(margin_left, available_height, line)

            available_height -= LINE_HEIGHT

        available_height -= SECTION_SPACING

        if key == "Cartuchos Apreendidos":
            break

    return page_number


def generate_pdf_file(operacao_uuid):
    global width_total, height_total, available_height
    width_total, height_total = 595, 841
    margin_left, content_width = 30, 535

    try:
        operacao_uuid = UUID(str(operacao_uuid))
        query_sql = load_query("op.identificador = %s")
        operacoes = Operacao.objects.raw(query_sql, [str(operacao_uuid)])
        attributes = operacoes[0].__dict__.copy()
        operation_name = attributes.get("Nome da operação", "Nome não disponível")
        attributes.pop("_state", None)
    except (Operacao.DoesNotExist, ValueError) as e:
        print(f"Erro ao buscar operação: {e}")
        return None

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(width_total, height_total))

    page_number = 1
    available_height = include_header(p, width_total)

    page_number = draw_first_page_content(p, margin_left, operation_name, content_width, FOOTER_HEIGHT, page_number)

    page_number = draw_operation_details(attributes, page_number, FOOTER_HEIGHT, p, content_width, margin_left)

    include_footer(p, width_total, page_number)
    p.save()
    buffer.seek(0)
    return buffer

