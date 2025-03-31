import datetime
import os
import logging
import uuid

from io import BytesIO
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.urls import reverse
from uuid import UUID
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from coredata.models import Bairro, Municipio
from operations.models import Operacao, UNIDADES_POLICIA, ORGAOS_EXTERNOS
from pathlib import Path
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

logger = logging.getLogger(__name__)

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

from django.http import JsonResponse

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


def format_and_exclud(atributos):
    for chave, valor in atributos.items():
        print(valor, type(valor))
 
    return atributos



def generate_pdf_file(operacaoUUID): 
    base_dir = Path(f"{settings.BASE_DIR}/query")  # Define o diretório base
    file_name = "query.sql"  # Nome do arquivo

    query = (base_dir / file_name).read_text()  # Lê a query do arquivo

    try:
        operacaoUUID = UUID(str(operacaoUUID))  
        operacoes = Operacao.objects.raw(query, [operacaoUUID])
        atributos = operacoes[0].__dict__.copy()
        atributos.pop("_state", None)
        # format_and_exclud(atributos)
        
    except (Operacao.DoesNotExist, ValueError) as e:
        print(f"Erro ao buscar operação: {e}")  
        return None  

    ## Inicia escrita no pdf
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # header
    img_header = os.path.join(settings.BASE_DIR, "static", "img", "bg-inicial-page.png")
    p.drawImage(img_header, 0, 760, width=600, height=88)
    
    # emitido em
    p.setFont("Helvetica", 12)
    p.drawString(400, 740, "Emitido em: ")
    hora = datetime.datetime.now()
    hora_formatada = hora.strftime("%d/%m/%Y %H:%M")
    p.drawString(400 + stringWidth("Emitido em: ", "Helvetica", 12), 740, hora_formatada)

    # visualizar operacao
    p.setFont("Helvetica-Bold", 14)
    p.drawString(25, 720, "Visualizar operação")
    
    # atributos do documento
    y = 690 
    pagina = 1
    # for atributos in lista_atributos:  # Percorre todas as operações encontradas
    for chave, valor in atributos.items():
        
        p.setFont("Helvetica-Bold", 12)
        p.drawString(25, y, f"{chave}")
        p.setFont("Helvetica", 12)
        p.drawString(25 + stringWidth(chave, "Helvetica-Bold", 12), y, f": {valor}")
        y -= 20  # Reduz o espaço vertical para próxima linha

        # Se a margem inferior for atingida, cria uma nova página
        if y < 50:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(260, 20, f"Página {pagina}")
            p.showPage()
            y = 750  # Reseta para o topo da nova página

            pagina += 1

        if chave == "Cartuchos Apreendidos":
            break
        y -= 10  # Adiciona um espaço extra entre cada operação

    p.showPage()
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