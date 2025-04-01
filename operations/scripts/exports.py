import os
from uuid import UUID

from django.conf import settings
from django.template import Template, Context
from datetime import date, datetime, time
from io import BytesIO
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from operations.models import Operacao



def date_or_time_formatter(data):
    if isinstance(data, datetime): 
        return data.strftime("%d/%m/%Y %H:%M")  
    elif isinstance(data, date):  
        return data.strftime("%d/%m/%Y") 
    elif isinstance(data, time): 
        return data.strftime("%H:%M")
    return data



def include_header(p, width, is_first_page=False):
    img_header = os.path.join(settings.BASE_DIR, "static", "img", "bg-inicial-page.png")
    p.drawImage(img_header, 0, heightTotal - 88, width=width, height=88)
    
    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#353535"))
    total_text = "Emitido em: " + date_or_time_formatter(datetime.now())
    
    totaltext_y = heightTotal - 88 - 40 
    p.drawString(
        width - stringWidth(total_text, "Helvetica", 12) - 30,
        totaltext_y, 
        total_text
    )
    
    protected_area = 20 
    
    if is_first_page:
        return totaltext_y - protected_area - 80
    else:
        return totaltext_y - protected_area



def include_footer(p, width, n):
    pg_number = f"Página {n}" 
    
    p.setStrokeColor(HexColor("#F7CF32"))
    p.setLineWidth(10)
    p.line(0, 0, width, 0)  
    
    p.setFont("Helvetica", 10)
    p.drawString(
        width - stringWidth(pg_number, "Helvetica", 10) - 30, 
        15, 
        pg_number
    )



def load_query(where_condition=None):
    query_path = os.path.join(settings.BASE_DIR, 'query', 'query.sql')
    
    with open(query_path, 'r', encoding='utf-8') as file:
        query_sql = file.read()
    
    if where_condition:
        return query_sql.replace('/* WHERE_CONDITION */', f'WHERE {where_condition}')
    return query_sql.replace('/* WHERE_CONDITION */', '')



def break_text(text, max_width, font_size=12, is_bold=False):
    text = str(text) if not isinstance(text, str) else text
    font = "Helvetica-Bold" if is_bold else "Helvetica"
    lines = []
    current_line = []
    current_width = 0
    
    for word in text.split():
        word_width = stringWidth(word + ' ', font, font_size)
        
        if stringWidth(word, font, font_size) > max_width:
            temp_word = ''
            for char in word:
                char_width = stringWidth(char, font, font_size)
                if current_width + char_width <= max_width:
                    temp_word += char
                    current_width += char_width
                else:
                    if temp_word:
                        current_line.append(temp_word)
                        lines.append(' '.join(current_line))
                    current_line = []
                    current_width = 0
                    temp_word = char
                    current_width += char_width
            if temp_word:
                current_line.append(temp_word)
        else:
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def generate_pdf_file(operacaoUUID):
    global widthTotal, heightTotal
    widthTotal, heightTotal = 595, 841
    
    margin_left = (widthTotal - 535) / 2 
    content_width = 535 
    
    try:
        operacaoUUID = UUID(str(operacaoUUID))  
        where_condition = "op.identificador = %s"
        query_sql = load_query(where_condition)
        operacoes = Operacao.objects.raw(query_sql, [str(operacaoUUID)])        
        attributes = operacoes[0].__dict__.copy()
        attributes.pop("_state", None)
        
    except (Operacao.DoesNotExist, ValueError) as e:
        print(f"Erro ao buscar operação: {e}")  
        return None  

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(widthTotal, heightTotal))
    
    pg_number = 1
    available_height = include_header(p, widthTotal, is_first_page=True)
    
    footer_height = 35
    min_height = footer_height
    
    p.setFont("Helvetica-Bold", 16)
    titulo = "Visualizar operação"
    p.drawString(margin_left, available_height, titulo)
    available_height -= 30 
    
    p.setStrokeColor(HexColor("#F7CF32"))
    p.setLineWidth(2)
    p.line(margin_left, available_height, margin_left + content_width, available_height)
    available_height -= 30
    
    line_height = 14
    space_betw_items = 10
    
    ignored_keys = ["id", "Criado em", "Seção Atual", "Dado registrado fora do sistema", "Cadastro Completo"]
    special_keys = [
        "Justificativa da excepcionalidade da operação",
        "Objetivo estratégico da operação", 
        "Análise de riscos e medidas de controle"
    ]
    
    for key, value in attributes.items():
        if key in ignored_keys:
            continue
        
        shown_value = ("não preenchido" if value is None or value == "" or value == " " else
                      "sim" if isinstance(value, bool) and value else
                      "não" if isinstance(value, bool) else
                      "programada" if value == "Pr" else
                      "emergencial" if value == "Em" else
                      str(date_or_time_formatter(value)) if isinstance(value, (date, datetime)) else
                      str(value))
        
        if available_height < min_height + line_height:
            include_footer(p, widthTotal, pg_number)
            p.showPage()
            pg_number += 1
            available_height = include_header(p, widthTotal)
        
        if key in special_keys:
            p.setFont("Helvetica-Bold", 12)
            key_lines = break_text(key + ":", content_width, is_bold=True)
            
            for line in key_lines:
                if available_height < min_height + line_height:
                    include_footer(p, widthTotal, pg_number)
                    p.showPage()
                    pg_number += 1
                    available_height = include_header(p, widthTotal)
                    p.setFont("Helvetica-Bold", 12)
                
                p.drawString(margin_left, available_height, line)
                available_height -= line_height
            
            # VALUE em linha separada
            p.setFont("Helvetica", 12)
            value_lines = break_text(shown_value, content_width)
            
            for line in value_lines:
                if available_height < min_height + line_height:
                    include_footer(p, widthTotal, pg_number)
                    p.showPage()
                    pg_number += 1
                    available_height = include_header(p, widthTotal)
                    p.setFont("Helvetica", 12)
                
                p.drawString(margin_left, available_height, line)
                available_height -= line_height
        else:
            complete_text = f"{key}: {shown_value}"
            p.setFont("Helvetica-Bold", 12)
            key_part = f"{key}: "
            key_width = stringWidth(key_part, "Helvetica-Bold", 12)
            
            p.drawString(margin_left, available_height, key_part)
            
            p.setFont("Helvetica", 12)
            value_lines = break_text(shown_value, content_width - key_width, font_size=12)
            
            if value_lines:
                p.drawString(margin_left + key_width, available_height, value_lines[0])
                
                for line in value_lines[1:]:
                    available_height -= line_height
                    if available_height < min_height + line_height:
                        include_footer(p, widthTotal, pg_number)
                        p.showPage()
                        pg_number += 1
                        available_height = include_header(p, widthTotal)
                        p.setFont("Helvetica", 12)
                    p.drawString(margin_left, available_height, line)
            
            available_height -= line_height
        
        available_height -= space_betw_items
        
        if key == "Cartuchos Apreendidos":
            break
    
    include_footer(p, widthTotal, pg_number)
    p.save()
    buffer.seek(0)
    return buffer
