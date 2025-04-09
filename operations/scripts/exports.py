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


class BaseReportFormatter:
    IGNORED_KEYS = [
        "id",
        "identificador",
        "Criado em",
        "Seção Atual",
        "Dado registrado fora do sistema",
        "Cadastro Completo",
        "Nome da operação"
    ]

    def list_ignored_keys(self):
        return self.IGNORED_KEYS

    def format_value_for_display(self, value):
        if value is None or str(value).strip() == "":
            return "Não preenchido"
        if isinstance(value, bool):
            return "Sim" if value else "Não"
        if value == "Pr":
            return "Programada"
        if value == "Em":
            return "Emergencial"
        return str(value)

    def get_data(self, columns, result):
        """Retorna dados formatados como lista de listas (tabela)."""
        return [
            [self.format_value_for_display(getattr(row, col)) for col in columns if col]
            for row in result
        ]


class ExcelReport(BaseReportFormatter):
    def generate_excel_file(self, rows, header, sheet_title):
        """Cria e retorna um arquivo Excel em memória."""
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = sheet_title

        sheet.append(header)
        for row in rows:
            sheet.append(row)

        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)
        return buffer


class DetailReport(BaseReportFormatter):
    BIG_TEXT_COLUMNS = [
        "Justificativa da excepcionalidade da operação",
        "Objetivo estratégico da operação",
        "Análise de riscos e medidas de controle",
        "Endereço de referência",
        "Observações gerais"
    ]

    END_OF_SECTION_COLUMNS = [
        "Número do procedimento (TJRJ)",
        "Localidade",
        "Justificativa da excepcionalidade da operação",
        "Unidades Apoiadoras",
        "Análise de riscos e medidas de controle",
        "Número de veículos recuperados?"
    ]

    def get_data(self, columns, result):
        """Retorna dados formatados como tuplas (label, valor)."""
        instance = result[0]
        return [(col, self.format_value_for_display(getattr(instance, col))) for col in columns]

    def get_nome_operacao(self, data):
        """Retorna o valor da coluna 'Nome da operação' baseado na posição 3."""
        return data[3][1] if len(data) > 3 else "Não informado"

    def get_identificador(self, data):
        """Retorna o valor da coluna 'identificador' baseado na posição 0."""
        return data[0][1] if data else "Não informado"

    def get_columns_big_text(self):
        return self.BIG_TEXT_COLUMNS

    def get_columns_end_of_section(self):
        return self.END_OF_SECTION_COLUMNS


class PDFReport(BaseReportFormatter):
    # Constantes de layout
    PAGE_WIDTH = 595
    PAGE_HEIGHT = 841
    MARGIN_LEFT = 30
    CONTENT_WIDTH = 535
    HEADER_HEIGHT = 82
    FOOTER_HEIGHT = 35
    LINE_HEIGHT = 12
    SECTION_SPACING = 12


    def __init__(self):
        self.canvas = None
        self.page_number = 1
        self.available_height = self.PAGE_HEIGHT
        self.buffer = BytesIO()

    def get_data(self, result):
        data = result[0].__dict__.copy()
        data.pop("_state", None)
        return data

    def set_canvas(self):
        self.canvas = canvas.Canvas(self.buffer, pagesize=(self.PAGE_WIDTH, self.PAGE_HEIGHT))

    def set_style(self, font="Helvetica", size=12, color="#505050"):
        self.canvas.setFont(font, size)
        self.canvas.setFillColor(HexColor(color))

    def break_text(self, text, max_width, font_size=12, is_bold=False):
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

    def include_header(self):
        img_header = os.path.join(settings.BASE_DIR, "static", "img", "bg-inicial-page.png")
        self.canvas.drawImage(img_header, 0, self.PAGE_HEIGHT - self.HEADER_HEIGHT, width=self.PAGE_WIDTH, height=self.HEADER_HEIGHT)

        self.set_style(size=12, color="#353535")
        emitido_em = f"Emitido em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        y = self.PAGE_HEIGHT - self.HEADER_HEIGHT - 23
        self.canvas.drawString(self.PAGE_WIDTH - stringWidth(emitido_em, "Helvetica", 12) - 30, y, emitido_em)

        self.available_height = y - 32

    def include_footer(self):
        self.canvas.setStrokeColor(HexColor("#F7CF32"))
        self.canvas.setLineWidth(10)
        self.canvas.line(0, 0, self.PAGE_WIDTH, 0)

        self.set_style(size=10)
        pg_text = f"Página {self.page_number}"
        self.canvas.drawString(self.PAGE_WIDTH - stringWidth(pg_text, "Helvetica", 10) - 30, 15, pg_text)

    def new_page(self):
        self.include_footer()
        self.canvas.showPage()
        self.page_number += 1
        self.include_header()

    def ensure_space(self, required_height):
        if self.available_height < self.FOOTER_HEIGHT + required_height:
            self.new_page()

    def draw_title(self, title):
        self.set_style("Helvetica-Bold", 14)
        self.canvas.drawString(self.MARGIN_LEFT, self.available_height, title)
        self.available_height -= 26

    def draw_operation_name(self, operation_name):
        self.set_style("Helvetica-Bold", 10, "#9F9F9F")
        for line in self.break_text(operation_name, self.CONTENT_WIDTH, font_size=10, is_bold=True):
            self.ensure_space(10)
            self.canvas.drawString(self.MARGIN_LEFT, self.available_height, line)
            self.available_height -= 10

        self.canvas.setStrokeColor(HexColor("#F7CF32"))
        self.canvas.setLineWidth(1)
        self.canvas.line(self.MARGIN_LEFT, self.available_height - 5, self.MARGIN_LEFT + self.CONTENT_WIDTH, self.available_height - 5)
        self.available_height -= 30

    def draw_key_value_block(self, key, value, is_special=False):
        shown_value = self.format_value_for_display(value)

        if is_special:
            self.set_style("Helvetica-Bold", 12)
            for line in self.break_text(f"{key}:", self.CONTENT_WIDTH, is_bold=True):
                self.ensure_space(self.LINE_HEIGHT)
                self.canvas.drawString(self.MARGIN_LEFT, self.available_height, line)
                self.available_height -= self.LINE_HEIGHT * 2

            self.set_style("Helvetica", 12)
            for line in self.break_text(shown_value, self.CONTENT_WIDTH):
                self.ensure_space(self.LINE_HEIGHT)
                self.canvas.drawString(self.MARGIN_LEFT, self.available_height, line)
                self.available_height -= self.LINE_HEIGHT * 2
        else:
            key_text = f"{key}: "
            key_width = stringWidth(key_text, "Helvetica-Bold", 12)

            self.ensure_space(self.LINE_HEIGHT)
            self.set_style("Helvetica-Bold", 12)
            self.canvas.drawString(self.MARGIN_LEFT, self.available_height, key_text)

            value_lines = self.break_text(shown_value, self.CONTENT_WIDTH - key_width)
            if value_lines:
                self.set_style("Helvetica", 12)
                self.canvas.drawString(self.MARGIN_LEFT + key_width, self.available_height, value_lines[0])
                for line in value_lines[1:]:
                    self.available_height -= self.LINE_HEIGHT
                    self.ensure_space(self.LINE_HEIGHT)
                    self.canvas.drawString(self.MARGIN_LEFT, self.available_height, line)

            self.available_height -= self.LINE_HEIGHT

        self.available_height -= self.SECTION_SPACING

    def draw_operation_details(self, attributes):
        ignored_keys = self.list_ignored_keys()
        special_keys = {
            "Justificativa da excepcionalidade da operação",
            "Objetivo estratégico da operação",
            "Análise de riscos e medidas de controle"
        }

        for key, value in attributes.items():
            if key in ignored_keys:
                continue
            self.draw_key_value_block(key, value, key in special_keys)

            if key == "Cartuchos Apreendidos":
                break

    def generate_pdf_file(self, operacoes):
        operation_name = operacoes.get("Nome da operação", "Nome não disponível")

        self.set_canvas()
        self.include_header()

        self.draw_title("Visualizar operação")
        self.draw_operation_name(operation_name)
        self.draw_operation_details(operacoes)

        self.include_footer()
        self.canvas.save()
        self.buffer.seek(0)
        return self.buffer

