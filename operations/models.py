from django.conf import settings
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from users.models import User
from operations.exceptions import OperationNotCompleteException
from operations.mail import notifica_por_email


class InformacaoManager(models.Manager):
    def get_obj_or_none(self, usuario, identificador):
        try:
            obj = self.get(usuario=usuario, indentificador=identificador)
        except models.ObjectDoesNotExist:
            obj = None

        return obj


class LocalidadeOperacao(models.Model):
    localidade = models.CharField("Localidade", max_length=255, null=True, blank=True) 
    municipio = models.CharField("Município", max_length=255, null=True, blank=True)
    bairro = models.CharField("Bairro", max_length=255, null=True, blank=True)
    endereco_referencia = models.CharField("Endereço de referência", max_length=255, null=True, blank=True)


class UnidadesApoiadores(models.Model):
    nome_unidade = models.CharField("Unidade Apoiadora", max_length=255, null=True, blank=True)


class OrgaosExternosOperacao(models.Model):
    nome_orgao = models.CharField("Órgão Externo", max_length=255, null=True, blank=True)


class TiposDeDroga(models.Model):
    nome_droga = models.CharField("Nome da Droga", max_length=255, null=True, blank=True)


class CartuchoCalibresApreendidos(models.Model):
    tipo_cartucho = models.CharField("Tipo de Cartucho", max_length=255, null=True, blank=True)
    tipo_calibre = models.CharField("Tipo de Calibre", max_length=255, null=True, blank=True)


class ROApensado(models.Model):
    numero_ro = models.CharField("Número do RO", max_length=255, null=True, blank=True)


class Operacao(models.Model):
    n_sections = 10

    objects = InformacaoManager()

    history = HistoricalRecords(
        verbose_name="Histórico de alterações da operação",
        excluded_fields=["secao_atual"]
    )

    SITUACAO_INCOMPLETO = "incompleto"
    SITUACAO_CSO = "completo sem ocorrencia"
    SITUACAO_CCO = "completo com ocorrencia"
    SITUACAO_CADASTRO = [
        (SITUACAO_INCOMPLETO, "Incompleto"),
        (SITUACAO_CSO, "Completo sem Ocorrência"),
        (SITUACAO_CCO, "Completo com Ocorrência"),
    ]
    NATUREZA_OPERACAO = [
        ("NatO I", "Ações de inteligência"),
        ("NatO II", "Cumprimento de Medidas Cautelares Judiciais"),
        ("NatO III", "Apoio operacional a outras instituições"),
        ("NatO IV", "Prestação de auxílio e assistência em emergências"),
    ]
    TIPO_OPERACAO = [
        ("Pr", "Programada"),
        ("Em", "Emergencial"),
    ]

    ### Status cadastro
    secao_atual = models.PositiveIntegerField("Seção Atual", default=1)
    completo = models.BooleanField("Cadastro Completo", default=False)
    situacao = models.CharField(
        "Situação Cadastro",
        max_length=100,
        choices=SITUACAO_CADASTRO,
        default=SITUACAO_INCOMPLETO
    )
    registro_anterior = models.BooleanField(
        "Dado registrado fora do sistema",
        default=False
    )

    identificador = models.UUIDField(unique=True, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    ### Info Registro
    # Caso tipo seja Pr - Programada
    numero_inquerito_mae = models.CharField(
        "Número do Inquérito Policial mãe",
        max_length=100,
        null=True,
        blank=True,
    )
    numero_tjrj = models.CharField(
        "Número do procedimento (TJRJ)",
        max_length=20,
        null=True,
        blank=True
    )
    tipo_operacao = models.CharField(
        "Tipo de operação",
        choices=TIPO_OPERACAO,
        max_length=10,
        null=True
    )
    nome_operacao = models.CharField("Nome da operação", max_length=255, null=True, blank=True)

    ### Info Gerais One
    data = models.DateField("Data", null=True, blank=True)
    hora_inicio = models.TimeField("Hora de início da operação", null=True, blank=True)
    hora_termino = models.TimeField("Hora de término da operação", null=True, blank=True)
    localidade_operacao = models.ManyToManyField(LocalidadeOperacao)


    ### Info Gerais Two
    justificativa_excepcionalidade_operacao = models.TextField(
        "Justificativa da excepcionalidade da operação",
        null=True,
        blank=True
    )
    objetivo_estrategico_operacao = models.TextField(
        "Objetivo estratégico da operação",
        null=True,
        blank=True
    )


    ### Info Operacionais One
    nome_delegado_operacao = models.CharField("Nome do Delegado Responsável", max_length=255, null=True, blank=True)
    matricula_id_delegado_operacao = models.CharField("Matrícula/ID Funcional do Delegado", max_length=10, null=True, blank=True)
    natureza_operacao = models.CharField(
        "Natureza da operação",
        choices=NATUREZA_OPERACAO,
        max_length=10,
        null=True
    )
    unidade_responsavel = models.CharField("Unidade da polícia judiciária responsável", max_length=255, null=True, blank=True)
    # apoio_recebido = models.BooleanField(
    #     "Recebeu apoio de outras unidades policiais?",
    #     default=False
    # )
    unidades_apoiadoras = models.ManyToManyField(UnidadesApoiadores)
    # operacao_integrada = models.BooleanField(
    #     "Operação integrada com órgãos externos à Polícia Civil?",
    #     default=False
    # )
    orgaos_externos = models.ManyToManyField(OrgaosExternosOperacao)
    
    
    ### Info Operacionais Two
    numero_viaturas_mobilizadas = models.PositiveIntegerField(
        "Número de viaturas mobilizadas",
        default=0,
        blank=True
    )
    numero_agentes_mobilizados = models.PositiveIntegerField(
        "Número de agentes mobilizados",
        default=1,
        blank=True
    )
    numero_veiculos_blindados = models.PositiveIntegerField(
        "Número de veículos blindados",
        default=0,
        blank=True
    )
    numero_aeronaves = models.PositiveIntegerField(
        "Número de aeronaves",
        default=0,
        blank=True
    )
    numero_equipes_medicas = models.PositiveIntegerField(
        "Número de equipes médicas de apoio",
        default=0,
        blank=True
    )
    comunicou_escolas_saude = models.BooleanField(
        "Comunicou a equipamentos de saúde e escolas?",
        null=True,
        blank=True,
    )
    escolas_perto = models.BooleanField(
        "Escolas nas proximidades?",
        null=True,
        blank=True,
    )
    hospitais_perto = models.BooleanField(
        "Hospitais nas proximidades?",
        null=True,
        blank=True,
    )
    descricao_analise_risco = models.TextField(
        "Análise de riscos e medidas de controles de danos colaterais das operações e de disparos de confrontos",
        null=True,
        blank=True
    )


    ### Info Resultados One
    # Caso tipo seja Em - Emergencial
    registro_ocorrencia = models.ManyToManyField(ROApensado)
    houve_confronto_daf = models.BooleanField(
        "Houve confronto com DAF?",
        null=True,
        blank=True,
    )
    houve_resultados_operacao = models.BooleanField(
        "Houve resultados na operação?",
        null=True,
        blank=True,
    )
    numero_presos_elencados = models.PositiveIntegerField(
        "Número de presos elencados nos mandados de prisão",
        default=0,
        blank=True
    )
    numero_presos_outros_mandados = models.PositiveIntegerField(
        "Número de presos indicados em outros mandados de prisão pendentes",
        default=0,
        blank=True
    )
    numero_presos_flagrante = models.PositiveIntegerField(
        "Número de presos em flagrante",
        default=0,
        blank=True
    )
    numero_adolescentes_apreendidos = models.PositiveIntegerField(
        "Número de adolescentes apreendidos",
        default=0,
        blank=True,
    )
    numero_policiais_feridos = models.PositiveIntegerField(
        "Número de policiais feridos",
        default=0,
        blank=True,
    )
    numero_mortes_policiais = models.PositiveIntegerField(
        "Número de mortes policiais",
        default=0,
        blank=True
    )
    numero_mortes_interv_estado = models.PositiveIntegerField(
        "Número de mortes por intervenção de agentes do Estado",
        default=0,
        blank=True
    )
    numero_civis_mortos = models.PositiveIntegerField(
        "Número de civis mortos",
        default=0,
        blank=True
    )
    numero_civis_feridos = models.PositiveIntegerField(
        "Número de civis feridos",
        default=0,
        blank=True
    )
    numero_civis_mortos_npap = models.PositiveIntegerField(
        "Número de civis mortos – morte não provocada por agente policiais",
        default=0,
        blank=True
    )
    numero_veiculos_recuperados = models.PositiveIntegerField(
        "Número de veículos recuperados",
        default=0,
        blank=True
    )
    houve_apreensao_drogas = models.BooleanField(
        "Houve apreensão de Drogas?",
        null=True,
        blank=True,
    )
    tipos_drogas_apreendidas = models.ManyToManyField(TiposDeDroga)


    ### Info Resultados Two
    numero_explosivos_apreendidos = models.PositiveIntegerField(
        "Número de artefatos explosivos apreendidos",
        default=0,
        blank=True
    )
    numero_armas_apreendidas = models.PositiveIntegerField(
        "Número de armas apreendidas",
        default=0,
        blank=True
    )
    numero_fuzis_apreendidos = models.PositiveIntegerField(
        "Número de fuzis apreendidos",
        default=0,
        blank=True
    )
    numero_carregadores_apreendidos = models.PositiveIntegerField(
        "Número de carregadores apreendidos",
        default=0,
        blank=True
    )
    numero_municoes_apreendidas = models.PositiveIntegerField(
        "Número de munições apreendidas",
        default=0,
        blank=True
    )
    cartuchos_calibres = models.ManyToManyField(CartuchoCalibresApreendidos)
    
    
    # Info Resultados Three
    houve_disparados_aeronave = models.BooleanField(
        "Houve disparos embarcado da aeronave?",
        null=True,
        blank=True,
    )
    houve_registros_imagem = models.BooleanField(
        "Foram feitos registros de imagem a partir da aeronave?",
        null=True,
        blank=True
    )
    local_preservado = models.BooleanField(
        "Local permaneceu preservado?",
        null=True,
        blank=True
    )
    pericia_local = models.BooleanField(
        "Foi feita perícia do local?",
        null=True,
        blank=True
    )
    pericia_aeronave = models.BooleanField(
        "Foi feita perícia da aeronave?",
        null=True,
        blank=True
    )
    pericia_veiculo_blindado = models.BooleanField(
        "Foi feita perícia do veículo blindado?",
        null=True,
        blank=True
    )
    pericia_viaturas = models.BooleanField(
        "Foi feita perícia das viaturas?",
        null=True,
        blank=True
    )
    pericia_iml = models.BooleanField(
        "Foi feita perícia no IML?",
        null=True,
        blank=True
    )
    pericia_outras = models.BooleanField(
        "Foram feitas outras perícias?",
        null=True,
        blank=True
    )
    observacoes_gerais = models.TextField(
        "Observações gerais",
        null=True,
        blank=True
    )


    class Meta:
        db_table = "operacao"
        verbose_name = "operação"
        verbose_name_plural = "operações"

        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_nr_fuzis_menorigual_nr_armas",
                check=models.Q(numero_fuzis_apreendidos__lte=models.F("numero_armas_apreendidas")),
            )
        ]

    @property
    def get_admin_url(self):
        path = reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=[self.id]
        )
        return f"{settings.SITE_URL}{path}"

    def update_section(self, new_section):
        self.secao_atual = new_section
        self.save()

        return self.secao_atual

    def make_complete(self):
        if self.completo is False:
            self.completo = True
            self.notify_completion()

        self.situacao = self.SITUACAO_CSO
        # if self.houve_ocorrencia_operacao is True:
        #     self.situacao = self.SITUACAO_CCO

        self.save()

    def notify_completion(self):
        if self.completo is False:
            raise OperationNotCompleteException

        if not settings.DEBUG:
            notifica_por_email(self)
