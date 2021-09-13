from django.urls import path

from operations import views

app_name = "operations"
urlpatterns = [
    path("cadastro/", views.OperationReportView.as_view(), name="form"),
    path("progress/", views.OperationReportView.as_view(), name="progress"),
    path(
        "cadastro/<uuid:form_uuid>",
        views.UpdateOperationReportView.as_view(),
        name="form-update"
    ),
    path(
        "cadastro/informacoes/gerais/parte-1/<uuid:form_uuid>",
        views.OperationGeneralInfoPageOneView.as_view(),
        name="form-general-info-page-one"
    ),
    path(
        "cadastro/informacoes/gerais/parte-2/<uuid:form_uuid>",
        views.OperationGeneralInfoPageTwoView.as_view(),
        name="form-general-info-page-two"
    ),
    path(
        "cadastro/informacoes/operacionais/parte-1/<uuid:form_uuid>",
        views.OperationInfoPageOneView.as_view(),
        name="form-operational-info-page-one"
    ),
    path(
        "cadastro/informacoes/operacionais/parte-2/<uuid:form_uuid>",
        views.OperationInfoPageTwoView.as_view(),
        name="form-operational-info-page-two"
    ),
    path(
        "cadastro/informacoes/etapa-1-concluida/<uuid:form_uuid>",
        views.OperationFirstStageFinishedView.as_view(),
        name="form-first-stage-finished"
    ),
    path(
        "cadastro/informacoes/resultado/parte-1/<uuid:form_uuid>",
        views.OperationResultsPageOneView.as_view(),
        name="form-info-result-page-one"
    ),
    path(
        "cadastro/informacoes/resultado/parte-2/<uuid:form_uuid>",
        views.OperationResultsPageTwoView.as_view(),
        name="form-info-result-page-two"
    ),
    path(
        "cadastro/informacoes/resultado/parte-3/<uuid:form_uuid>",
        views.OperationResultsPageThreeView.as_view(),
        name="form-info-result-page-three"
    ),
    # path(
    #     "cadastro/informacoes/observacoes/<uuid:form_uuid>",
    #     views.OperationGeneralObservation.as_view(),
    #     name="form-observacoes-gerais"
    # ),
    path(
        "cadastro/completo/<uuid:form_uuid>",
        views.FormCompleteView.as_view(),
        name="form-complete"
    ),
    path("lista/", views.OperationListView.as_view(), name="operations-list"),
    path("painel/", views.PanelListView.as_view(), name="operations-panel"),
]
