import re

from rest_framework import serializers

from coredata.models import Batalhao, Bairro
from operations.models import (
    Operacao,
    LocalidadeOperacao,
    UnidadesApoiadores,
    OrgaosExternosOperacao,
    TiposDeDroga,
    CartuchoCalibresApreendidos,
    ROApensado
)


class OperacaoSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            instance.__setattr__(key, val)

        instance.save()
        return instance


class OperationRegisterInfoSerializer(OperacaoSerializer):
    numero_inquerito_mae = serializers.CharField(allow_blank=True)
    tipo_operacao = serializers.CharField(required=True)
    nome_operacao = serializers.CharField(required=True)
    numero_tjrj = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["tipo_operacao"] == "Pr" and not attrs["numero_inquerito_mae"]:
            raise serializers.ValidationError(
                {"numero_inquerito_mae": "Número de inquérito mãe deve ser fornecido para operação de tipo Programada."}
            )
        return attrs


class InfoGeralOperacaoOneSerializer(OperacaoSerializer):
    
    class LocalidadeOperacaoSerializer(OperacaoSerializer):
        localidade = serializers.CharField(required=True)
        municipio = serializers.CharField(required=True)
        bairro = serializers.CharField(required=True)
        endereco_referencia = serializers.CharField(required=True)

        def validate(self, attrs):
            # bairros_validos = Bairro.objects.get_ordered_for_municipio(
            #     attrs["municipio"]
            # ).values_list("bairro", flat=True)

            # if attrs["bairro"] not in bairros_validos:
            #     raise serializers.ValidationError(
            #         {"bairro": "Bairro inválido para município selecionado."}
            #     )
            return attrs

        # class Meta:
        #     model = LocalidadeOperacao
        #     fields = '__all__'

    data = serializers.DateField(format="%Y-%m-%d", required=True)
    hora_inicio = serializers.TimeField(format="%H:%M:%S", required=True)
    hora_termino = serializers.TimeField(format="%H:%M:%S", required=True)
    localidade_operacao = LocalidadeOperacaoSerializer(many=True)

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            if key == 'localidade_operacao':
                loc_instances = []
                for loc_obj in val:
                    loc_instances.append(LocalidadeOperacao.objects.create(**loc_obj))
                instance.localidade_operacao.clear()
                instance.localidade_operacao.add(*loc_instances)
            else:
                instance.__setattr__(key, val)

        instance.save()
        return instance


class InfoGeralOperacaoTwoSerializer(OperacaoSerializer):
    justificativa_excepcionalidade_operacao = serializers.CharField(required=True)
    objetivo_estrategico_operacao = serializers.CharField(required=True)


class InfoOperacionaisOperacaoOneSerializer(OperacaoSerializer):
    class UnidadeApoiadoraSerializer(OperacaoSerializer):
        nome_unidade = serializers.CharField(required=True)

    class OrgaoExternoSerializer(OperacaoSerializer):
        nome_orgao = serializers.CharField(required=True)

    nome_delegado_operacao = serializers.CharField(required=True)
    matricula_id_delegado_operacao = serializers.CharField(required=True)
    natureza_operacao = serializers.CharField(required=True)
    unidade_responsavel = serializers.CharField(required=True)
    apoio_recebido = serializers.BooleanField(required=True)
    unidades_apoiadoras = UnidadeApoiadoraSerializer(many=True)
    operacao_integrada = serializers.BooleanField(required=True)
    orgaos_externos = OrgaoExternoSerializer(many=True)

    # def validate_matricula_id_delegado_operacao(self, value):
    #     match = re.match(r"\d{5,6}", value)
    #     if not match:
    #         raise serializers.ValidationError("Número RG PM inválido.")

    #     return value


    def validate(self, attrs):
        # unidades_validas = Bairro.objects.get_ordered_for_municipio(
        #     attrs["municipio"]
        # ).values_list("bairro", flat=True)

        # if attrs["unidade_responsavel"] not in unidades_validas:
        #     raise serializers.ValidationError(
        #         {"unidade_responsavel": "Bairro inválido para município selecionado."}
        #     )

        return attrs

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            if key == 'unidades_apoiadoras':
                loc_instances = []
                for loc_obj in val:
                    loc_instances.append(UnidadesApoiadores.objects.create(**loc_obj))
                instance.unidades_apoiadoras.clear()
                instance.unidades_apoiadoras.add(*loc_instances)
            elif key == 'orgaos_externos':
                loc_instances = []
                for loc_obj in val:
                    loc_instances.append(OrgaosExternosOperacao.objects.create(**loc_obj))
                instance.orgaos_externos.clear()
                instance.orgaos_externos.add(*loc_instances)
            else:
                instance.__setattr__(key, val)

        instance.save()
        return instance


class InfoOperacionaisOperacaoTwoSerializer(OperacaoSerializer):
    numero_viaturas_mobilizadas = serializers.IntegerField(required=True, min_value=0)
    numero_agentes_mobilizados = serializers.IntegerField(required=True, min_value=1)
    numero_veiculos_blindados = serializers.IntegerField(required=True, min_value=0)
    numero_aeronaves = serializers.IntegerField(required=True, min_value=0)
    numero_equipes_medicas = serializers.IntegerField(required=True, min_value=0)
    descricao_analise_risco = serializers.CharField(required=True)


class InfoResultadosOneSerializer(OperacaoSerializer):
    class ROApensadoSerializer(OperacaoSerializer):
        numero_ro = serializers.CharField(required=True)

    registro_ocorrencia = ROApensadoSerializer(many=True)
    houve_confronto_daf = serializers.BooleanField(required=True)
    houve_resultados_operacao = serializers.BooleanField(required=True)
    # houve_ocorrencia_operacao = serializers.BooleanField(required=True)
    numero_presos_elencados = serializers.IntegerField(required=True, min_value=0)
    numero_presos_flagrante = serializers.IntegerField(required=True, min_value=0)
    numero_adolescentes_apreendidos = serializers.IntegerField(required=True, min_value=0)
    numero_policiais_feridos = serializers.IntegerField(required=True, min_value=0)
    numero_mortes_policiais = serializers.IntegerField(required=True, min_value=0)
    numero_civis_mortos = serializers.IntegerField(required=True, min_value=0)
    # numero_mortes_interv_estado = serializers.IntegerField(required=True, min_value=0)
    numero_civis_feridos = serializers.IntegerField(required=True, min_value=0)
    # numero_civis_mortos_npap = serializers.IntegerField(required=True, min_value=0)
    numero_veiculos_recuperados = serializers.IntegerField(required=True, min_value=0)

    def validate(self, attrs):
        # Verifica se já existem dados de ocorrência
        # ser = InfoOcorrenciaOneSerializer(instance=self.instance)
        # has_occurence_data = any(ser.data.values())

        # Precisa verificar se tem registro de ocorrência caso seja Em
        # if attrs["tipo_operacao"] == "Em" and not attrs["numero_ordem_operacoes"]:
        #     raise serializers.ValidationError(
        #         {"numero_ordem_operacoes": "Número da ordem deve ser fornecido."}
        #     )

        # if (
        #     self.instance.houve_ocorrencia_operacao and not
        #     attrs["houve_ocorrencia_operacao"] and
        #     has_occurence_data is True
        # ):
        #     msg = "Operação com ocorrência não pode ser atualizada para sem ocorrência."
        #     raise serializers.ValidationError(
        #         {
        #             "houve_ocorrencia_operacao": msg
        #         }
        #     )
        return attrs

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            if key == 'registro_ocorrencia':
                loc_instances = []
                for loc_obj in val:
                    loc_instances.append(ROApensado.objects.create(**loc_obj))
                instance.registro_ocorrencia.clear()
                instance.registro_ocorrencia.add(*loc_instances)
            else:
                instance.__setattr__(key, val)

        instance.save()
        return instance


class InfoResultadosTwoSerializer(OperacaoSerializer):
    class CartuchoCalibreSerializer(OperacaoSerializer):
        tipo_cartucho = serializers.CharField(required=True)
        tipo_calibre = serializers.CharField(required=True)

    droga_cocaina = serializers.BooleanField(required=True)
    droga_cannabis = serializers.BooleanField(required=True)
    droga_haxixe = serializers.BooleanField(required=True)
    droga_sinteticos = serializers.BooleanField(required=True)
    droga_outros = serializers.BooleanField(required=True)
    numero_explosivos_apreendidos = serializers.IntegerField(required=True, min_value=0)
    numero_armas_apreendidas = serializers.IntegerField(required=True, min_value=0)
    numero_fuzis_apreendidos = serializers.IntegerField(required=True, min_value=0)
    # numero_presos = serializers.IntegerField(required=True, min_value=0)
    numero_carregadores_apreendidos = serializers.IntegerField(required=True, min_value=0)
    numero_municoes_apreendidas = serializers.IntegerField(required=True, min_value=0)
    cartuchos_calibres = CartuchoCalibreSerializer(many=True)

    # def validate_registro_ocorrencia(self, value):
    #     match = re.match(r"^\d{3}-\d{5}/\d{4}(-\d{2})?$", value)
    #     if not match:
    #         raise serializers.ValidationError("Número de RO inválido.")

    #     return value

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            if key == 'cartuchos_calibres':
                loc_instances = []
                for loc_obj in val:
                    loc_instances.append(CartuchoCalibresApreendidos.objects.create(**loc_obj))
                instance.cartuchos_calibres.clear()
                instance.cartuchos_calibres.add(*loc_instances)
            else:
                instance.__setattr__(key, val)

        instance.save()
        return instance


class InfoResultadosThreeSerializer(OperacaoSerializer):
    houve_disparados_aeronave = serializers.BooleanField(required=True)
    houve_registros_imagem = serializers.BooleanField(required=True)
    local_preservado = serializers.BooleanField(required=True)
    pericia_local = serializers.BooleanField(required=True)
    pericia_aeronave = serializers.BooleanField(required=True)
    pericia_veiculo_blindado = serializers.BooleanField(required=True)
    pericia_viaturas = serializers.BooleanField(required=True)
    pericia_iml = serializers.BooleanField(required=True)
    pericia_outras = serializers.BooleanField(required=True)
    observacoes_gerais = serializers.CharField(allow_blank=True)


class OperacaoEmailSerializer(serializers.ModelSerializer):
    data = serializers.DateField(format="%d/%m/%Y")
    tipo_operacao = serializers.CharField(source="get_tipo_operacao_display")
    operacao_admin_url = serializers.URLField(source="get_admin_url")

    class Meta:
        model = Operacao
        fields = (
            "localidade_operacao",
            "unidade_responsavel",
            "data",
            "tipo_operacao",
            "objetivo_estrategico_operacao",
            "operacao_admin_url",
        )
