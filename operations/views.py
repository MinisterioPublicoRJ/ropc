import os
import uuid

from datetime import date, datetime, time
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.urls import reverse
from io import BytesIO
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from uuid import UUID

from coredata.models import Bairro, Municipio
from operations.models import Operacao, UNIDADES_POLICIA, ORGAOS_EXTERNOS
from operations.serializers import (
    OperationRegisterInfoSerializer,
    InfoGeralOperacaoOneSerializer,
    InfoGeralOperacaoTwoSerializer,
    InfoOperacionaisOperacaoOneSerializer,
    InfoOperacionaisOperacaoTwoSerializer,
    InfoResultadosOneSerializer,
    InfoResultadosTwoSerializer,
    InfoResultadosThreeSerializer
)

URL_SECTION_MAPPER = {
    1: "operations:form-update",
    2: "operations:form-general-info-page-one",
    3: "operations:form-general-info-page-two",
    4: "operations:form-operational-info-page-one",
    5: "operations:form-operational-info-page-two",
    6: "operations:form-first-stage-finished",
    7: "operations:form-info-result-page-one",
    8: "operations:form-info-result-page-two",
    9: "operations:form-info-result-page-three",
    10: "operations:form-complete",
}


class OperationReportView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_uuid"] = uuid.uuid4()
        context["operacao_data"] = dict()
        context["tipos_operacoes"] = Operacao.TIPO_OPERACAO
        return context


class OperationViewMixin:
    def get_serialized_data(self, operacao):
        return self.serializer_class(operacao).data

    def dispatch(self, request, *args, **kwargs):
        # TODO: Refatorar essa lógica
        self.form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        self.operacao = self.get_operation(self.request.user, self.form_uuid)
        # if (
        #     self.operacao.houve_ocorrencia_operacao is False and
        #     self.section_number == 7 and self.operacao.secao_atual == 8
        # ):
        #     dest_url = URL_SECTION_MAPPER[5]
        #     return redirect(
        #         reverse(dest_url, kwargs={"form_uuid": self.form_uuid})
        #     )

        # if (
        #     self.operacao.houve_ocorrencia_operacao is False and
        #     self.section_number in settings.SKIPPABLE_SECTIONS
        # ):
        #     self.operacao.update_section(OperationGeneralObservation.section_number)
        #     reverse_url = reverse(
        #         "operations:form-observacoes-gerais",
        #         kwargs={"form_uuid": self.form_uuid}
        #     )
        #     if request.path != reverse_url:
        #         return redirect(reverse_url)
        if self.section_number > self.operacao.secao_atual:
            secao_atual_url = URL_SECTION_MAPPER[self.operacao.secao_atual]
            return redirect(
                reverse(secao_atual_url, kwargs={"form_uuid": self.form_uuid})
            )

        handler = super().dispatch(request, *args, **kwargs)
        return handler

    def get_operation(self, usuario, form_uuid):
        return get_object_or_404(
            Operacao,
            identificador=form_uuid
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_uuid"] = self.form_uuid
        context["operacao_info"] = self.get_serialized_data(self.operacao)
        return context


# TODO: add tests
class UpdateOperationReportView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = OperationRegisterInfoSerializer

    section_number = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tipos_operacoes"] = Operacao.TIPO_OPERACAO
        return context


class OperationGeneralInfoPageOneView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_info_general_page_one.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoGeralOperacaoOneSerializer

    section_number = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nb_localidades"] = len(context["operacao_info"]["localidade_operacao"])
        context["municipios"] = Municipio.objects.get_ordered_values()
        context["bairros"] = []
        for i in range(context["nb_localidades"]):
            try:
                selected_municipio = context["operacao_info"]["localidade_operacao"][i]["municipio"]
            except:
                selected_municipio = context["municipios"][0]["nm_mun"]
            context[f"bairros_{i+1}"] = Bairro.objects.get_ordered_for_municipio(selected_municipio)
            context[f"bairros"].append(Bairro.objects.get_ordered_for_municipio(selected_municipio))
        if not context["nb_localidades"]:
            selected_municipio = context["municipios"][0]["nm_mun"]
            context[f"bairros_1"] = Bairro.objects.get_ordered_for_municipio(selected_municipio)
            context[f"bairros"].append(Bairro.objects.get_ordered_for_municipio(selected_municipio))

        return context


# TODO: add tests
class OperationGeneralInfoPageTwoView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_info_general_page_two.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoGeralOperacaoTwoSerializer

    section_number = 3


class OperationInfoPageOneView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_info_operation_page_one.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoOperacionaisOperacaoOneSerializer

    section_number = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["natureza_operacoes"] = Operacao.NATUREZA_OPERACAO
        context["unidades_policia_judiciaria"] = UNIDADES_POLICIA
        context["orgaos_externos"] = ORGAOS_EXTERNOS
        context["operacao_info"]["unidades_apoiadoras"] = [
            x['nome_unidade'] for x in context["operacao_info"]["unidades_apoiadoras"]
        ]
        context["operacao_info"]["orgaos_externos"] = [
            x['nome_orgao'] for x in context["operacao_info"]["orgaos_externos"]
        ]
        return context


class OperationInfoPageTwoView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_info_operation_page_two.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoOperacionaisOperacaoTwoSerializer

    section_number = 5


class OperationFirstStageFinishedView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_first_stage_finished.html"
    lookup_url_kwarg = "form_uuid"

    section_number = 6

    def get_context_data(self, **kwargs):
        self.form_uuid = self.kwargs.get(self.lookup_url_kwarg)

        context = super().get_context_data(**kwargs)
        context["form_uuid"] = self.form_uuid
        return context


class OperationResultsPageOneView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_results_page_one.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoResultadosOneSerializer

    section_number = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tipos_drogas"] = ["Cannabis", "Cocaína", "Outras"]
        context["operacao_info"]["registro_ocorrencia"] = ",".join(
            x['numero_ro'] for x in context["operacao_info"]["registro_ocorrencia"]
        )
        return context


class OperationResultsPageTwoView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_results_page_two.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoResultadosTwoSerializer

    section_number = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nb_cartuchos"] = len(context["operacao_info"]["cartuchos_calibres"])
        context["tipos_cartuchos"] = ["Plastico CBC", "Outros"]
        context["tipos_calibres"] = ["Calibre 28", "Outros"]
        return context


class OperationResultsPageThreeView(LoginRequiredMixin, OperationViewMixin, TemplateView):
    template_name = "operations/form_template_results_page_three.html"
    lookup_url_kwarg = "form_uuid"
    serializer_class = InfoResultadosThreeSerializer

    section_number = 9


class FormCompleteView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_complete.html"
    lookup_url_kwarg = "form_uuid"

    section_number = 10

    def get_serialized_data(self, operacao):
        return {}

    def dispatch(self, request, *args, **kwargs):
        # TODO: Refatorar essa lógica

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        self.form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        self.operacao = self.get_operation(self.request.user, self.form_uuid)

        secao_atual_url = URL_SECTION_MAPPER.get(self.operacao.secao_atual)

        # if self.operacao.houve_ocorrencia_operacao is None:
        #     return redirect(
        #         reverse(secao_atual_url, kwargs={"form_uuid": self.form_uuid})
        #     )
        #elif (
        if (
            # self.operacao.houve_ocorrencia_operacao is True and
            self.operacao.secao_atual < Operacao.n_sections
        ):
            return redirect(
                reverse(secao_atual_url, kwargs={"form_uuid": self.form_uuid})
            )

        handler = super().dispatch(request, *args, **kwargs)

        if self.operacao.secao_atual == Operacao.n_sections + 1:
            return handler
        if (
            self.operacao.secao_atual == Operacao.n_sections
            # and self.operacao.houve_ocorrencia_operacao is True
        ):
            return handler
            # return redirect(
            #     reverse(secao_atual_url, kwargs={"form_uuid": self.form_uuid})
            # )
        # if (
        #     self.operacao.secao_atual == Operacao.n_sections
        #     and self.operacao.houve_ocorrencia_operacao is False
        # ):
        #     return handler
        # if (
        #     self.operacao.secao_atual in settings.SKIPPABLE_SECTIONS
        #     and self.operacao.houve_ocorrencia_operacao is False
        # ):
        #     return handler
        else:
            return redirect(
                reverse(secao_atual_url, kwargs={"form_uuid": self.form_uuid})
            )

    def get_operation(self, usuario, form_uuid):
        return get_object_or_404(
            Operacao,
            identificador=form_uuid
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        self.operacao = self.get_operation(self.request.user, form_uuid)
        context["form_uuid"] = form_uuid
        context["operacao_info"] = self.get_serialized_data(self.operacao)
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.operacao.make_complete()
        return response


class OperationListView(LoginRequiredMixin, ListView):
    template_name = "operations/operations_list_template.html"
    paginate_by = settings.OPERATIONS_PER_PAGE

    # def get_queryset(self):
    #     return Operacao.objects.order_by("-criado_em")
    model = Operacao

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        queryset = Operacao.objects.order_by("-criado_em")
        if query:
            queryset = queryset.filter(nome_operacao__icontains=query)  # Ajuste o campo conforme o modelo
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Verifica se é uma requisição AJAX
            resultados = [{"id": op.id, "nome_operacao": op.nome_operacao} for op in self.get_queryset()]
            return JsonResponse(resultados, safe=False)
        return super().render_to_response(context, **response_kwargs)


class InitialPageListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/initial_page_template.html"



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



def generate_pdf(request, identificador):
    try:
        identificador = UUID(str(identificador))  
        logger.info(f"UUID recebido na view (convertido): {identificador} ({type(identificador)})")

        buffer = generate_pdf_file(identificador)
        if not buffer:
            return HttpResponse("Erro ao gerar o PDF. Operação não encontrada.", status=404)

        return FileResponse(buffer, as_attachment=True, filename='operacao.pdf')

    except ValueError as e:
        logger.error(f"UUID inválido recebido: {identificador}. Erro: {e}")
        return HttpResponse("UUID inválido.", status=400)

    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {e}")
        return HttpResponse(f"Erro interno do servidor: {e}", status=500)