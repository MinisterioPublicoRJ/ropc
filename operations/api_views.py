from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from operations.mixins import AllowPUTAsCreateMixin
from operations.models import Operacao
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


class RegistrationInfoViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OperationRegisterInfoSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 2

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )

    def get_operation(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        objs = Operacao.objects.filter(identificador=identificador)
        if objs:
            obj = get_object_or_404(objs, usuario=user)
        else:
            obj = Operacao.objects.create(identificador=identificador, usuario=user)

        return obj


class GeneralInfoOneViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoGeralOperacaoOneSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 3

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )

    def get_operation(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        objs = Operacao.objects.filter(identificador=identificador)
        if objs:
            obj = get_object_or_404(objs, usuario=user)
        else:
            obj = Operacao.objects.create(identificador=identificador, usuario=user)

        return obj

    def preprocess_data(self, data):
        processed_data = {}

        processed_data['data'] = data['data']
        processed_data['hora_inicio'] = data['hora_inicio']
        processed_data['hora_termino'] = data['hora_termino']
        processed_data['localidade_operacao'] = []

        nb_fields = len(data.keys())
        nb_location_fields = nb_fields - 3
        nb_location_objs = int(nb_location_fields/4)

        for i in range(1, nb_location_objs+1):
            loc_obj = {}

            obj_keys = [k for k in data.keys() if str(i) in k]
            for k in obj_keys:
                loc_obj[k.split('-')[0]] = data[k]

            processed_data['localidade_operacao'].append(loc_obj)

        return processed_data


class GeneralInfoTwoViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoGeralOperacaoTwoSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 4

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )


class OperationalInfoOneViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoOperacionaisOperacaoOneSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 5

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )

    def preprocess_data(self, data):
        ### Modificar com unidades apoiadoras e orgaos externos
        processed_data = {}

        processed_data['nome_delegado_operacao'] = data['nome_delegado_operacao']
        processed_data['matricula_id_delegado_operacao'] = data['matricula_id_delegado_operacao']
        processed_data['natureza_operacao'] = data['natureza_operacao']
        processed_data['unidade_responsavel'] = data['unidade_responsavel']
        processed_data['apoio_recebido'] = data['apoio_recebido']
        processed_data['operacao_integrada'] = data['operacao_integrada']
        processed_data['unidades_apoiadoras'] = [{'nome_unidade': x} for x in data['unidades_apoiadoras']]
        processed_data['orgaos_externos'] = [{'nome_orgao': x} for x in data['orgaos_externos']]

        # nb_fields = len(data.keys())
        # nb_location_fields = nb_fields - 3
        # nb_location_objs = int(nb_location_fields/4)
        # print(data)
        # for i in range(1, nb_location_objs+1):
        #     loc_obj = {}

        #     obj_keys = [k for k in data.keys() if str(i) in k]
        #     for k in obj_keys:
        #         loc_obj[k.split('-')[0]] = data[k]

        #     processed_data['localidade_operacao'].append(loc_obj)

        return processed_data

class OperationalInfoTwoViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoOperacionaisOperacaoTwoSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 7

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )


class ResultInfoOneViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoResultadosOneSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 8

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )
    
    def preprocess_data(self, data):
        ### Modificar com ros
        processed_data = {}

        processed_data['houve_confronto_daf'] = data['houve_confronto_daf']
        processed_data['houve_resultados_operacao'] = data['houve_resultados_operacao']
        processed_data['numero_presos_elencados'] = data['numero_presos_elencados']
        processed_data['numero_presos_outros_mandados'] = data['numero_presos_outros_mandados']
        processed_data['numero_presos_flagrante'] = data['numero_presos_flagrante']
        processed_data['numero_adolescentes_apreendidos'] = data['numero_adolescentes_apreendidos']
        processed_data['numero_policiais_feridos'] = data['numero_policiais_feridos']
        processed_data['numero_mortes_policiais'] = data['numero_mortes_policiais']
        processed_data['numero_civis_mortos'] = data['numero_civis_mortos']
        processed_data['numero_civis_feridos'] = data['numero_civis_feridos']
        processed_data['numero_veiculos_recuperados'] = data['numero_veiculos_recuperados']

        processed_data['registro_ocorrencia'] = []
        registros = data['registro_ocorrencia'].split(',')
        for ro in registros:
            processed_data['registro_ocorrencia'].append({'numero_ro': ro})

        return processed_data


class ResultInfoTwoViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoResultadosTwoSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 9

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )

    def preprocess_data(self, data):
        ### Modificar com cartuchocalibre
        processed_data = {}

        processed_data['droga_cocaina'] = False if not data['droga_cocaina'] else True
        processed_data['droga_cannabis'] = False if not data['droga_cannabis'] else True
        processed_data['droga_haxixe'] = False if not data['droga_haxixe'] else True
        processed_data['droga_sinteticos'] = False if not data['droga_sinteticos'] else True
        processed_data['droga_outros'] = False if not data['droga_outros'] else True
        processed_data['numero_explosivos_apreendidos'] = data['numero_explosivos_apreendidos']
        processed_data['numero_municoes_apreendidas'] = data['numero_municoes_apreendidas']
        processed_data['numero_carregadores_apreendidos'] = data['numero_carregadores_apreendidos']
        processed_data['numero_armas_apreendidas'] = data['numero_armas_apreendidas']
        processed_data['numero_fuzis_apreendidos'] = data['numero_fuzis_apreendidos']
        processed_data['cartuchos_calibres'] = []

        nb_fields = len(data.keys())
        nb_cartucho_fields = nb_fields - 10
        nb_cartucho_objs = int(nb_cartucho_fields/2)

        for i in range(1, nb_cartucho_objs+1):
            cart_obj = {}

            obj_keys = [k for k in data.keys() if str(i) in k]
            for k in obj_keys:
                cart_obj[k.split('-')[0]] = data[k]

            processed_data['cartuchos_calibres'].append(cart_obj)

        return processed_data


class ResultInfoThreeViewSet(AllowPUTAsCreateMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InfoResultadosThreeSerializer
    lookup_url_kwarg = "form_uuid"
    lookup_field = "identificador"
    model_class = Operacao

    next_section_number = 10

    def get_operation(self):
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            Operacao,
            identificador=identificador,
            usuario=self.request.user,
        )

    def get_queryset(self):
        user = self.request.user
        identificador = self.kwargs.get(self.lookup_url_kwarg)
        return Operacao.objects.filter(
            usuario=user,
            identificador=identificador
        )

    def preprocess_data(self, data):
        ### Modificar com cartuchocalibre
        processed_data = {}

        processed_data['houve_disparados_aeronave'] = data['houve_disparados_aeronave']
        processed_data['houve_registros_imagem'] = data['houve_registros_imagem']
        processed_data['local_preservado'] = data['local_preservado']
        processed_data['pericia_local'] = False if not data['pericia_local'] else True
        processed_data['pericia_aeronave'] = False if not data['pericia_aeronave'] else True
        processed_data['pericia_veiculo_blindado'] = False if not data['pericia_veiculo_blindado'] else True
        processed_data['pericia_viaturas'] = False if not data['pericia_viaturas'] else True
        processed_data['pericia_iml'] = False if not data['pericia_iml'] else True
        processed_data['pericia_outras'] = False if not data['pericia_outras'] else True
        processed_data['observacoes_gerais'] = data['observacoes_gerais']

        return processed_data


# class GeneralObservationViewSet(AllowPUTAsCreateMixin, ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = GeneralObservationSerializer
#     lookup_url_kwarg = "form_uuid"
#     lookup_field = "identificador"
#     model_class = Operacao

#     next_section_number = 9

#     def get_operation(self):
#         identificador = self.kwargs.get(self.lookup_url_kwarg)
#         return get_object_or_404(
#             Operacao,
#             identificador=identificador,
#             usuario=self.request.user,
#         )

#     def get_queryset(self):
#         user = self.request.user
#         identificador = self.kwargs.get(self.lookup_url_kwarg)
#         return Operacao.objects.filter(
#             usuario=user,
#             identificador=identificador
#         )
