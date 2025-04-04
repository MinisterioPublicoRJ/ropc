import uuid

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView
from django.views import View
from django.urls import reverse
from io import BytesIO
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
from .scripts.exports import gera_planilha_excel, generate_pdf_file
from collections import defaultdict
from datetime import datetime 


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

    model = Operacao

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        queryset = Operacao.objects.order_by("-criado_em")
        if query:
            queryset = queryset.filter(nome_operacao__icontains=query)  
     
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query_params"] = self.request.GET  
        return context

class GenereteReportView(LoginRequiredMixin, View):
    def get_data(self, columns, result):
        return [tuple([str(getattr(row, col)) for col in columns]) for row in result]


    def get(self, request):
        result = Operacao.objects.get_operations_report()
        
        columns = result.query.get_columns()
        print(columns)               
        data = self.get_data(columns, result)
        excel_buffer = gera_planilha_excel(data, columns, "Operações")

        date_now =datetime.now().strftime("%d_%m_%Y %H:%M:%S")
        return FileResponse(excel_buffer, filename=f"Operações ROPC até {date_now}.xlsx", as_attachment=True)


class OperationDetailView(LoginRequiredMixin, View):
    template_name = "operations/operation_detail.html"
    lookup_url_kwarg = "form_uuid"

    def get_data(self, columns, result):
        return [(col,str(getattr(result[0], col))) for col in columns]

    def get(self, request, *args, **kwargs):
        form_uuid = self.kwargs.get(self.lookup_url_kwarg)  # Obtém o UUID da URL
        
        # Obtém o conjunto de dados a partir do método customizado
        result = Operacao.objects.get_operations_report(form_uuid)
  
        columns = result.query.get_columns()
        data = self.get_data(columns, result)
        nome_operacao = data[4][1]
        identificador = data[0][1]
   
        columns_with_big_text = [
                                "Justificativa da excepcionalidade da operação", 
                                "Objetivo estratégico da operação",
                                "Análise de riscos e medidas de controle",
                                "Endereço de referência", 
                                "Observações gerais"
                                ]
        
        columns_end_section =   [
                                "Número do procedimento (TJRJ)", 
                                "Localidade", 
                                "Justificativa da excepcionalidade da operação", 
                                "Unidades Apoiadoras",
                                "Análise de riscos e medidas de controle", 
                                "Número de veículos recuperados?"
                                ]
        
        ignored_keys = [
                        "identificador"
                        "id",
                        "Criado em",
                        "Seção Atual",
                        "Dado registrado fora do sistema",
                        "Cadastro Completo",
                        "Nome da operação"
                        ]
                        
        context = {
            "detail": data, 
            "datetime_now": datetime.now(),
            "columns_with_big_text": columns_with_big_text,
            "columns_end_section": columns_end_section,
            "ignored_keys": ignored_keys,
            "nome_operacao": nome_operacao,
            "identificador": identificador
        }

       
        return render(request, self.template_name, context)

class InitialPageListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/initial_page_template.html"



def generate_pdf(request, identificador):
    #result = Operacao.objects.get_operations_report(form_uuid) TODO fazer query aqui

    try:
        identificador = UUID(str(identificador))

        buffer = generate_pdf_file(identificador)
        if not buffer:
            return HttpResponse("Erro ao gerar o PDF. Operação não encontrada.", status=404)

        return FileResponse(buffer, as_attachment=True, filename='operacao.pdf')

    except ValueError as e:
        return HttpResponse("UUID inválido.", status=400)

    except Exception as e:
        return HttpResponse(f"Erro interno do servidor: {e}", status=500)



