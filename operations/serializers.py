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
    numero_tjrj = serializers.CharField(allow_blank=True)

    def validate(self, attrs):
        errs = {}
        # if attrs["tipo_operacao"] == "Pr" and not attrs["numero_inquerito_mae"]:
        #     errs["numero_inquerito_mae"] = "Número de inquérito mãe deve ser fornecido para operação de tipo Programada."
        if attrs["numero_tjrj"] and (not attrs["numero_tjrj"].isdigit() or len(attrs["numero_tjrj"]) != 20):
            errs["numero_tjrj"] = "Número do TJRJ deve consistir de 20 dígitos."
        if attrs["numero_inquerito_mae"] and (not attrs["numero_inquerito_mae"].isdigit() or len(attrs["numero_inquerito_mae"]) != 12):
            errs["numero_inquerito_mae"] = "Número do inquérito mãe deve consistir de 12 dígitos."
        if errs:
            raise serializers.ValidationError(errs)
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

        def to_internal_value(self, data):
            try:
                return super().to_internal_value(data)
            except serializers.ValidationError as exer:
                err = exer.__dict__
                err['detail']['loc_position'] = data['loc_position']
                raise serializers.ValidationError(err)


    data = serializers.DateField(format="%Y-%m-%d", required=True)
    hora_inicio = serializers.TimeField(format="%H:%M:%S", required=True)
    hora_termino = serializers.TimeField(format="%H:%M:%S", required=True)
    localidade_operacao = LocalidadeOperacaoSerializer(many=True, required=True)

    def validate(self, attrs):
        errs = {}
        if len(attrs['localidade_operacao']) < 1:
            errs["localidade-1"] = "É necessário fornecer pelo menos uma localidade!"
        if errs:
            raise serializers.ValidationError(errs)
        return attrs

    def is_valid(self, raise_exception=False):
        try:
            super().is_valid(raise_exception)
        except serializers.ValidationError as exer:
            errs = exer.__dict__['detail']
            if 'localidade_operacao' in errs:
                details = exer.__dict__['detail']['localidade_operacao']
                for det in details:
                    if not det:
                        continue
                    pos = det['detail']['loc_position']
                    keys = [k for k in det['detail'] if k != 'loc_position']
                    for k in keys:
                        errs[f'{k}-{pos}'] = det['detail'][k]
                errs.pop('localidade_operacao')
            raise serializers.ValidationError(errs)

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

    def validate_matricula_id_delegado_operacao(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Número de matrícula deve ser numérico.")

        return value


    def validate(self, attrs):
        errs = {}
        if attrs['apoio_recebido'] and not attrs['unidades_apoiadoras']:
            errs["unidades_apoiadoras"] = "Apoio recebido sem unidades apoiadoras selecionadas!"
        if not attrs['apoio_recebido'] and attrs['unidades_apoiadoras']:
            errs["unidades_apoiadoras"] = "Unidades apoiadoras selecionadas, porém apoio recebido marcado como não!"
        if attrs['operacao_integrada'] and not attrs['orgaos_externos']:
            errs["orgaos_externos"] = "Operação integrada sem órgãos externos selecionados!"
        if not attrs['operacao_integrada'] and attrs['orgaos_externos']:
            errs["orgaos_externos"] = "Órgãos externos selecionados para operação não integrada!"
        if errs:
            raise serializers.ValidationError(errs)
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
    comunicou_escolas_saude = serializers.BooleanField(required=True)
    escolas_perto = serializers.BooleanField(required=True)
    hospitais_perto = serializers.BooleanField(required=True)
    descricao_analise_risco = serializers.CharField(required=True)


class InfoResultadosOneSerializer(OperacaoSerializer):
    class ROApensadoSerializer(OperacaoSerializer):
        numero_ro = serializers.CharField(required=True)

        def validate_numero_ro(self, value):
            if not value.isdigit():
                raise serializers.ValidationError("Número de registro de ocorrência deve ser numérico.")
            if len(value) != 12:
                raise serializers.ValidationError("Número de registro de ocorrência deve ter 12 dígitos.")

            return value

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

    def is_valid(self, raise_exception=False):
        try:
            super().is_valid(raise_exception)
        except serializers.ValidationError as exer:
            errs = exer.__dict__['detail']
            if 'registro_ocorrencia' in errs:
                details = exer.__dict__['detail']['registro_ocorrencia']
                ro_errs = []
                for det in details:
                    if not det:
                        continue
                    ro_errs.append(det['numero_ro'][0])
                    break
                errs['registro_ocorrencia'] = ro_errs
            raise serializers.ValidationError(errs)

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

        def to_internal_value(self, data):
            try:
                return super().to_internal_value(data)
            except serializers.ValidationError as exer:
                err = exer.__dict__
                err['detail']['cart_position'] = data['cart_position']
                raise serializers.ValidationError(err)

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

    def is_valid(self, raise_exception=False):
        try:
            super().is_valid(raise_exception)
        except serializers.ValidationError as exer:
            errs = exer.__dict__['detail']
            if 'cartuchos_calibres' in errs:
                details = exer.__dict__['detail']['cartuchos_calibres']
                for det in details:
                    if not det:
                        continue
                    pos = det['detail']['cart_position']
                    keys = [k for k in det['detail'] if k != 'cart_position']
                    for k in keys:
                        errs[f'{k}-{pos}'] = det['detail'][k]
                errs.pop('cartuchos_calibres')
            raise serializers.ValidationError(errs)

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
