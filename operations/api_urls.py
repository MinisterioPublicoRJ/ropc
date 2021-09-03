from django.urls import path

from operations import api_views


single_actions = {
    "get": "retrieve",
    "put": "update",
}


app_name = "operations_api"
urlpatterns = [
    path(
        "cria-informacoes-registro/<uuid:form_uuid>",
        api_views.RegistrationInfoViewSet.as_view(single_actions),
        name="create-registration-info"
    ),
    path(
        "cria-informacoes-gerais-parte-1/<uuid:form_uuid>",
        api_views.GeneralInfoOneViewSet.as_view(single_actions),
        name="create-general-info-1"
    ),
    path(
        "cria-informacoes-gerais-parte-2/<uuid:form_uuid>",
        api_views.GeneralInfoTwoViewSet.as_view(single_actions),
        name="create-general-info-2"
    ),
    path(
        "cria-informacoes-operacionais-parte-1/<uuid:form_uuid>",
        api_views.OperationalInfoOneViewSet.as_view(single_actions),
        name="create-operational-info-1"
    ),
    path(
        "cria-informacoes-operacionais-parte-2/<uuid:form_uuid>",
        api_views.OperationalInfoTwoViewSet.as_view(single_actions),
        name="create-operational-info-2"
    ),
    path(
        "cria-informacoes-resultado-parte-1/<uuid:form_uuid>",
        api_views.ResultInfoOneViewSet.as_view(single_actions),
        name="create-result-info-1"
    ),
    path(
        "cria-informacoes-resultado-parte-2/<uuid:form_uuid>",
        api_views.ResultInfoTwoViewSet.as_view(single_actions),
        name="create-result-info-2"
    ),
    path(
        "cria-informacoes-resultado-parte-3/<uuid:form_uuid>",
        api_views.ResultInfoThreeViewSet.as_view(single_actions),
        name="create-result-info-3"
    )
]
