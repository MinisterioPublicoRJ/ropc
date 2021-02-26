import uuid

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView

from coredata.models import Bairro, Batalhao, Municipio
from operations.models import (
    InformacaoGeralOperacao,
    InformacaoOperacionalOperacao,
)
from operations.serializers import (
    InformacaoGeralOperacaoSerializer,
    InformacaoOperacionalOperacaoSerializer,
)


class OperationReportView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_uuid"] = uuid.uuid4()
        context["municipios"] = Municipio.objects.get_ordered_values()
        nm_first_city = context["municipios"][0]["nm_mun"]
        context["bairros"] = Bairro.objects.get_ordered_for_municipio(nm_first_city)
        context["batalhoes"] = Batalhao.objects.get_ordered_for_municipio(nm_first_city)
        context["operacao_data"] = dict()
        return context


# TODO: add tests
class UpdateOperationReportView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template.html"
    lookup_url_kwarg = "form_uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["municipios"] = Municipio.objects.get_ordered_values()
        form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        context["form_uuid"] = form_uuid
        operacao_info = get_object_or_404(
            InformacaoGeralOperacao,
            operacao__identificador=form_uuid
        )
        operacao_data = InformacaoGeralOperacaoSerializer(operacao_info).data
        context["bairros"] = Bairro.objects.get_ordered_for_municipio(
            operacao_data["municipio"]
        )
        context["batalhoes"] = Batalhao.objects.get_ordered_for_municipio(
            operacao_data["municipio"]
        )
        context["operacao_data"] = operacao_data
        return context


# TODO: add tests
class OperationInfoPageOneView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_info_operation_page_one.html"
    lookup_url_kwarg = "form_uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        info_geral = get_object_or_404(
            InformacaoGeralOperacao.objects.select_related("operacao"),
            operacao__identificador=form_uuid
        )
        info_operacional = InformacaoOperacionalOperacao.objects.get_obj_or_none(
            info_geral.operacao
        )
        context["form_uuid"] = form_uuid
        context["postos_comandante"] = InformacaoOperacionalOperacao.POSTO_COMANDANTE
        context["info_operacional"] = InformacaoOperacionalOperacaoSerializer(
            info_operacional
        ).data
        return context


class OperationInfoPageTwoView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_info_operation_page_two.html"
    lookup_url_kwarg = "form_uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_uuid = self.kwargs.get(self.lookup_url_kwarg)
        get_object_or_404(
            InformacaoGeralOperacao.objects.select_related("operacao"),
            operacao__identificador=form_uuid
        )
        context["tipos_operacoes"] = InformacaoOperacionalOperacao.TIPO_OPERACAO
        context["tipos_acoes_repressivas"] = InformacaoOperacionalOperacao.TIPO_ACAO_REPRESSIVA
        return context


class OperationOcurrencePageOneView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_ocurrence_page_one.html"

class OperationOcurrencePageTwoView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_ocurrence_page_two.html"

class OperationListView(LoginRequiredMixin, ListView):
    template_name = "operations/operations_list_template.html"
    paginate_by = settings.OPERATIONS_PER_PAGE

    def get_queryset(self):
        return InformacaoGeralOperacao.objects.filter(
            operacao__usuario=self.request.user
        )


class InitialPageListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/initial_page_template.html"


class PanelListView(LoginRequiredMixin, TemplateView):
    template_name = "operations/panel_template.html"


class OperationInfoResultRegisterView(LoginRequiredMixin, TemplateView):
    template_name = "operations/form_template_result_info.html"
