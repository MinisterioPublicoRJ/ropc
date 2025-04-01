import os
from uuid import UUID

from django.conf import settings
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



def break_text(text, max_width, font_name="Helvetica", font_size=12):
    lines = []
    current_line = []
    current_width = 0
    
    for word in text.split():
        word_width = stringWidth(word + ' ', font_name, font_size)
        
        if stringWidth(word, font_name, font_size) > max_width:
            temp_word = ''
            for char in word:
                char_width = stringWidth(char, font_name, font_size)
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
        base_dir = Path(f"{settings.BASE_DIR}/query")
        query = (base_dir / "query.sql").read_text()
        operacaoUUID = UUID(str(operacaoUUID))  
        operacoes = Operacao.objects.raw(query, [operacaoUUID])
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
    
    p.setFont("Helvetica", 12)
    line_height = 14
    space_betw_items = 10
    
    ignored_keys = ["id", "Criado em", "Seção Atual", "Dado registrado fora do sistema", "Cadastro Completo"]
    
    for key, value in attributes.items():
        if key in ignored_keys:
            continue
        
        # Tratamento dos valores
        shown_value = ("não preenchido" if value is None or value == "" or value == " " else
                        "sim" if isinstance(value, bool) and value else
                        "não" if isinstance(value, bool) else
                        "programada" if value == "Pr" else
                        "emergencial" if value == "Em" else
                        date_or_time_formatter(value))
        
        complete_txt = f"{key}: {shown_value}"
        lines = break_text(complete_txt, content_width, "Helvetica", 12)
        
        for line in lines:
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
