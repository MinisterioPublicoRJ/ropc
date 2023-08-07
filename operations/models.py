from django.conf import settings
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from users.models import User
from operations.exceptions import OperationNotCompleteException
from operations.mail import notifica_por_email

UNIDADES_POLICIA = [
    ("001a.Delegacia de Policia", "001a.Delegacia de Policia"),
    ("004a.Delegacia de Policia", "004a.Delegacia de Policia"),
    ("005a.Delegacia de Polícia", "005a.Delegacia de Polícia"),
    ("006a.Delegacia de Policia", "006a.Delegacia de Policia"),
    ("007a.Delegacia de Policia", "007a.Delegacia de Policia"),
    ("008a.Delegacia de Polícia", "008a.Delegacia de Polícia"),
    ("009a.Delegacia de Policia", "009a.Delegacia de Policia"),
    ("010a.Delegacia de Policia", "010a.Delegacia de Policia"),
    ("011a.Delegacia de Policia", "011a.Delegacia de Policia"),
    ("012a.Delegacia de Policia", "012a.Delegacia de Policia"),
    ("013a.Delegacia de Polícia", "013a.Delegacia de Polícia"),
    ("014a.Delegacia de Policia", "014a.Delegacia de Policia"),
    ("015a.Delegacia de Policia", "015a.Delegacia de Policia"),
    ("016a.Delegacia de Policia", "016a.Delegacia de Policia"),
    ("017a.Delegacia de Policia", "017a.Delegacia de Policia"),
    ("018a.Delegacia de Policia", "018a.Delegacia de Policia"),
    ("019a.Delegacia de Policia", "019a.Delegacia de Policia"),
    ("020a.Delegacia de Policia", "020a.Delegacia de Policia"),
    ("021a.Delegacia de Policia", "021a.Delegacia de Policia"),
    ("022a.Delegacia de Policia", "022a.Delegacia de Policia"),
    ("023a.Delegacia de Policia", "023a.Delegacia de Policia"),
    ("024a.Delegacia de Policia", "024a.Delegacia de Policia"),
    ("025a.Delegacia de Policia", "025a.Delegacia de Policia"),
    ("026a.Delegacia de Policia", "026a.Delegacia de Policia"),
    ("027a.Delegacia de Policia", "027a.Delegacia de Policia"),
    ("028a.Delegacia de Policia", "028a.Delegacia de Policia"),
    ("029a.Delegacia de Policia", "029a.Delegacia de Policia"),
    ("030a.Delegacia de Policia", "030a.Delegacia de Policia"),
    ("031a.Delegacia de Policia", "031a.Delegacia de Policia"),
    ("032a.Delegacia de Policia", "032a.Delegacia de Policia"),
    ("033a.Delegacia de Policia", "033a.Delegacia de Policia"),
    ("034a.Delegacia de Policia", "034a.Delegacia de Policia"),
    ("035a.Delegacia de Polícia", "035a.Delegacia de Polícia"),
    ("036a.Delegacia de Policia", "036a.Delegacia de Policia"),
    ("037a.Delegacia de Policia", "037a.Delegacia de Policia"),
    ("038a.Delegacia de Policia", "038a.Delegacia de Policia"),
    ("039a.Delegacia de Policia", "039a.Delegacia de Policia"),
    ("040a.Delegacia de Policia", "040a.Delegacia de Policia"),
    ("041a.Delegacia de Policia", "041a.Delegacia de Policia"),
    ("042a.Delegacia de Polícia", "042a.Delegacia de Polícia"),
    ("043a.Delegacia de Polícia", "043a.Delegacia de Polícia"),
    ("044a.Delegacia de Policia", "044a.Delegacia de Policia"),
    ("045a.Delegacia de Policia", "045a.Delegacia de Policia"),
    ("048a.Delegacia de Policia", "048a.Delegacia de Policia"),
    ("050a.Delegacia de Policia", "050a.Delegacia de Policia"),
    ("051a.Delegacia de Policia", "051a.Delegacia de Policia"),
    ("052a.Delegacia de Policia", "052a.Delegacia de Policia"),
    ("053a.Delegacia de Policia", "053a.Delegacia de Policia"),
    ("054a.Delegacia de Policia", "054a.Delegacia de Policia"),
    ("055a.Delegacia de Policia", "055a.Delegacia de Policia"),
    ("056a.Delegacia de Policia", "056a.Delegacia de Policia"),
    ("057a.Delegacia de Policia", "057a.Delegacia de Policia"),
    ("058a.Delegacia de Policia", "058a.Delegacia de Policia"),
    ("059a.Delegacia de Policia", "059a.Delegacia de Policia"),
    ("060a.Delegacia de Policia", "060a.Delegacia de Policia"),
    ("061a.Delegacia de Policia", "061a.Delegacia de Policia"),
    ("062a.Delegacia de Policia", "062a.Delegacia de Policia"),
    ("063a.Delegacia de Polícia", "063a.Delegacia de Polícia"),
    ("064a.Delegacia de Policia", "064a.Delegacia de Policia"),
    ("065a.Delegacia de Policia", "065a.Delegacia de Policia"),
    ("066a.Delegacia de Policia", "066a.Delegacia de Policia"),
    ("067a.Delegacia de Polícia", "067a.Delegacia de Polícia"),
    ("070a.Delegacia de Polícia", "070a.Delegacia de Polícia"),
    ("071a.Delegacia de Policia", "071a.Delegacia de Policia"),
    ("072a.Delegacia de Policia", "072a.Delegacia de Policia"),
    ("073a.Delegacia de Policia", "073a.Delegacia de Policia"),
    ("074a.Delegacia de Policia", "074a.Delegacia de Policia"),
    ("075a.Delegacia de Policia", "075a.Delegacia de Policia"),
    ("076a.Delegacia de Policia", "076a.Delegacia de Policia"),
    ("077a.Delegacia de Policia", "077a.Delegacia de Policia"),
    ("078a.Delegacia de Policia", "078a.Delegacia de Policia"),
    ("079a.Delegacia de Policia", "079a.Delegacia de Policia"),
    ("081a.Delegacia de Policia", "081a.Delegacia de Policia"),
    ("082a.Delegacia de Policia", "082a.Delegacia de Policia"),
    ("088a.Delegacia de Policia", "088a.Delegacia de Policia"),
    ("089a.Delegacia de Policia", "089a.Delegacia de Policia"),
    ("090a.Delegacia de Policia", "090a.Delegacia de Policia"),
    ("091a.Delegacia de Policia", "091a.Delegacia de Policia"),
    ("092a.Delegacia de Policia", "092a.Delegacia de Policia"),
    ("093a.Delegacia de Policia", "093a.Delegacia de Policia"),
    ("094a.Delegacia de Policia", "094a.Delegacia de Policia"),
    ("095a.Delegacia de Policia", "095a.Delegacia de Policia"),
    ("096a.Delegacia de Policia", "096a.Delegacia de Policia"),
    ("097a.Delegacia de Policia", "097a.Delegacia de Policia"),
    ("098a.Delegacia de Policia", "098a.Delegacia de Policia"),
    ("099a.Delegacia de Policia", "099a.Delegacia de Policia"),
    ("100a.Delegacia de Policia", "100a.Delegacia de Policia"),
    ("101a.Delegacia de Policia", "101a.Delegacia de Policia"),
    ("104a.Delegacia de Policia", "104a.Delegacia de Policia"),
    ("105a.Delegacia de Policia", "105a.Delegacia de Policia"),
    ("106a.Delegacia de Policia", "106a.Delegacia de Policia"),
    ("107a.Delegacia de Policia", "107a.Delegacia de Policia"),
    ("108a.Delegacia de Policia", "108a.Delegacia de Policia"),
    ("109a.Delegacia de Policia", "109a.Delegacia de Policia"),
    ("110a.Delegacia de Policia", "110a.Delegacia de Policia"),
    ("111a.Delegacia de Policia", "111a.Delegacia de Policia"),
    ("112a.Delegacia de Policia", "112a.Delegacia de Policia"),
    ("118a.Delegacia de Policia", "118a.Delegacia de Policia"),
    ("119a.Delegacia de Polícia", "119a.Delegacia de Polícia"),
    ("120a.Delegacia de Policia", "120a.Delegacia de Policia"),
    ("121a.Delegacia de Policia", "121a.Delegacia de Policia"),
    ("122a.Delegacia de Policia", "122a.Delegacia de Policia"),
    ("123a.Delegacia de Policia", "123a.Delegacia de Policia"),
    ("124a.Delegacia de Policia", "124a.Delegacia de Policia"),
    ("125a.Delegacia de Policia", "125a.Delegacia de Policia"),
    ("126a.Delegacia de Polícia", "126a.Delegacia de Polícia"),
    ("127a.Delegacia de Polícia", "127a.Delegacia de Polícia"),
    ("128a.Delegacia de Policia", "128a.Delegacia de Policia"),
    ("129a.Delegacia de Policia", "129a.Delegacia de Policia"),
    ("130a.Delegacia de Polícia", "130a.Delegacia de Polícia"),
    ("132a.Delegacia de Polícia", "132a.Delegacia de Polícia"),
    ("134a.Delegacia de Policia", "134a.Delegacia de Policia"),
    ("135a.Delegacia de Policia", "135a.Delegacia de Policia"),
    ("136a.Delegacia de Policia", "136a.Delegacia de Policia"),
    ("137a.Delegacia de Policia", "137a.Delegacia de Policia"),
    ("138a.Delegacia de Policia", "138a.Delegacia de Policia"),
    ("139a.Delegacia de Policia", "139a.Delegacia de Policia"),
    ("140a.Delegacia de Policia", "140a.Delegacia de Policia"),
    ("141a.Delegacia de Policia", "141a.Delegacia de Policia"),
    ("142a.Delegacia de Policia", "142a.Delegacia de Policia"),
    ("143a.Delegacia de Policia", "143a.Delegacia de Policia"),
    ("144a.Delegacia de Policia", "144a.Delegacia de Policia"),
    ("145a.Delegacia de Policia", "145a.Delegacia de Policia"),
    ("146a.Delegacia de Policia", "146a.Delegacia de Policia"),
    ("147a.Delegacia de Polícia", "147a.Delegacia de Polícia"),
    ("148a.Delegacia de Polícia", "148a.Delegacia de Polícia"),
    ("151a.Delegacia de Policia", "151a.Delegacia de Policia"),
    ("152a.Delegacia de Polícia", "152a.Delegacia de Polícia"),
    ("153a.Delegacia de Policia", "153a.Delegacia de Policia"),
    ("154a.Delegacia de Policia", "154a.Delegacia de Policia"),
    ("155a.Delegacia de Policia", "155a.Delegacia de Policia"),
    ("156a.Delegacia de Policia", "156a.Delegacia de Policia"),
    ("157a.Delegacia de Policia", "157a.Delegacia de Policia"),
    ("158a.Delegacia de Policia", "158a.Delegacia de Policia"),
    ("159a.Delegacia de Policia", "159a.Delegacia de Policia"),
    ("165a.Delegacia de Policia", "165a.Delegacia de Policia"),
    ("166a.Delegacia de Policia", "166a.Delegacia de Policia"),
    ("167a.Delegacia de Policia", "167a.Delegacia de Policia"),
    ("168a.Delegacia de Policia", "168a.Delegacia de Policia"),
    ("901. DH Capital", "901. DH Capital"),
    ("861. DH Baixada Fluminense", "861. DH Baixada Fluminense"),
    ("951. DH Niterói/São Gonçalo", "951. DH Niterói/São Gonçalo"),
    ("943. DH Oeste", "943. DH Oeste"),
    ("912. DEAM - Centro", "912. DEAM - Centro"),
    ("916. DEAM - Oeste", "916. DEAM - Oeste"),
    ("999. DEAM - Jacarepaguá", "999. DEAM - Jacarepaguá"),
    ("913. DEAM - Niterói", "913. DEAM - Niterói"),
    ("928. DEAM - São Gonçalo", "928. DEAM - São Gonçalo"),
    ("914. DEAM - Duque de Caxias", "914. DEAM - Duque de Caxias"),
    ("915. DEAM - Nova Iguacu", "915. DEAM - Nova Iguacu"),
    ("954. DEAM - São João de Meriti", "954. DEAM - São João de Meriti"),
    ("998. DEAM - Belford Roxo", "998. DEAM - Belford Roxo"),
    ("959. DEAM - Angra dos Reis", "959. DEAM - Angra dos Reis"),
    ("956. DEAM - Cabo Frio", "956. DEAM - Cabo Frio"),
    ("958. DEAM - Campos dos Goytacazes", "958. DEAM - Campos dos Goytacazes"),
    ("955. DEAM - Nova Friburgo", "955. DEAM - Nova Friburgo"),
    ("996. DEAM - Volta Redonda", "996. DEAM - Volta Redonda"),
    ("202. CORE", "202. CORE"),
    ("924. DAIRJ", "924. DAIRJ"),
    ("907. DAS", "907. DAS"),
    ("905. DC-POLINTER", "905. DC-POLINTER"),
    ("947. DCAV", "947. DCAV"),
    ("911. DDEF - Delegacia de Defraudações", "911. DDEF - Delegacia de Defraudações"),
    ("957. DDPA - Descoberta de Paradeiros", "957. DDPA - Descoberta de Paradeiros"),
    ("933. DDSD", "933. DDSD"),
    ("930. DEAPTI", "930. DEAPTI"),
    ("906. DEAT", "906. DEAT"),
    ("920. DECON", "920. DECON"),
    ("962. DECRADI", "962. DECRADI"),
    ("902. DCOD - Combate às Drogas", "902. DCOD - Combate às Drogas"),
    ("921. DELFAZ", "921. DELFAZ"),
    ("925. DELTRAN", "925. DELTRAN"),
    ("250. DGCOR - NIC-LD", "250. DGCOR - NIC-LD"),
    ("919. DMMA", "919. DMMA"),
    ("903. DPCA - Centro", "903. DPCA - Centro"),
    ("917. DPCA - Niterói", "917. DPCA - Niterói"),
    ("200. DPMA", "200. DPMA"),
    ("405. DRACO", "405. DRACO"),
    ("932. DRAE", "932. DRAE"),
    ("929. DRCCSP", "929. DRCCSP"),
    ("218. DRCI", "218. DRCI"),
    ("946. DRCPIM", "946. DRCPIM"),
    ("904. DRF", "904. DRF"),
    ("908. DRFA", "908. DRFA"),
    ("918. DRFC", "918. DRFC"),
    ("DESARME", "DESARME"),
    ("CIAF - Coord. Investig. Agentes com Foro", "CIAF - Coord. Investig. Agentes com Foro"),
    ("COINPOL (Corregedoria)", "COINPOL (Corregedoria)"),
    ("242. Delegacia Supervisora", "242. Delegacia Supervisora"),
    ("253. Central de Garantias - Norte", "253. Central de Garantias - Norte"),
    ("OUTROS", "OUTROS"),
]
ORGAOS_EXTERNOS = [
    ("SEPM - BAC", "SEPM - BAC"),
    ("SEPM - BEPE", "SEPM - BEPE"),
    ("SEPM - BOPE", "SEPM - BOPE"),
    ("SEPM - BPCHOQUE", "SEPM - BPCHOQUE"),
    ("SEPM - BPTUR ", "SEPM - BPTUR "),
    ("SEPM - BPVE", "SEPM - BPVE"),
    ("SEPM - COE", "SEPM - COE"),
    ("SEPM - RECOM", "SEPM - RECOM"),
    ("MPRJ - CSI", "MPRJ - CSI"),
    ("MPRJ - GAECO", "MPRJ - GAECO"),
    ("MPRJ - GAESF", "MPRJ - GAESF"),
    ("MPRJ - Outros", "MPRJ - Outros"),
    ("Polícia Federal", "Polícia Federal"),
    ("Polícia Rodoviária Federal", "Polícia Rodoviária Federal"),
    ("2º BPM - Zona Sul", "2º BPM - Zona Sul"),
    ("3º BPM - Méier", "3º BPM - Méier"),
    ("4º BPM - Centro", "4º BPM - Centro"),
    ("5º BPM - Centro", "5º BPM - Centro"),
    ("6º BPM - Tijuca", "6º BPM - Tijuca"),
    ("7º BPM - São Gonçalo", "7º BPM - São Gonçalo"),
    ("8º BPM - Campos", "8º BPM - Campos"),
    ("9º BPM - Madureira", "9º BPM - Madureira"),
    ("10º BPM - Barra do Piraí", "10º BPM - Barra do Piraí"),
    ("11º BPM - Nova Friburgo", "11º BPM - Nova Friburgo"),
    ("12º BPM - Niterói", "12º BPM - Niterói"),
    ("14º BPM - Bangu", "14º BPM - Bangu"),
    ("15º BPM - Duque de Caxias", "15º BPM - Duque de Caxias"),
    ("16º BPM - Penha", "16º BPM - Penha"),
    ("17º BPM - Ilha do Governador", "17º BPM - Ilha do Governador"),
    ("18º BPM - Jacarepaguá", "18º BPM - Jacarepaguá"),
    ("19º BPM - Copacabana", "19º BPM - Copacabana"),
    ("20º BPM - Nova Iguaçu", "20º BPM - Nova Iguaçu"),
    ("21º BPM - São João de Meriti", "21º BPM - São João de Meriti"),
    ("22º BPM - Bonsucesso", "22º BPM - Bonsucesso"),
    ("23º BPM - Zona Sul", "23º BPM - Zona Sul"),
    ("24º BPM - Queimados", "24º BPM - Queimados"),
    ("25º BPM - Região dos Lagos", "25º BPM - Região dos Lagos"),
    ("26º BPM - Petrópolis", "26º BPM - Petrópolis"),
    ("27º BPM - Santa Cruz", "27º BPM - Santa Cruz"),
    ("28º BPM - Volta Redonda", "28º BPM - Volta Redonda"),
    ("29º BPM - Itaperuna", "29º BPM - Itaperuna"),
    ("30º BPM - Teresópolis", "30º BPM - Teresópolis"),
    ("31º BPM - Barra da Tijuca", "31º BPM - Barra da Tijuca"),
    ("32º BPM - Rio das Ostras", "32º BPM - Rio das Ostras"),
    ("33º BPM - Angra dos Reis", "33º BPM - Angra dos Reis"),
    ("34º BPM - Magé", "34º BPM - Magé"),
    ("35º BPM - Rio Bonito", "35º BPM - Rio Bonito"),
    ("36º BPM - Cambuci", "36º BPM - Cambuci"),
    ("37º BPM - Resende", "37º BPM - Resende"),
    ("38º BPM - Três Rios", "38º BPM - Três Rios"),
    ("39º BPM - Belford Roxo", "39º BPM - Belford Roxo"),
    ("40º BPM - Campo Grande", "40º BPM - Campo Grande"),
    ("41º BPM - Irajá", "41º BPM - Irajá"),
    ("Outros", "Outros"),
]


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
    nome_unidade = models.CharField("Unidade Apoiadora", choices=UNIDADES_POLICIA, max_length=255, null=True,
                                    blank=True)


class OrgaosExternosOperacao(models.Model):
    nome_orgao = models.CharField("Órgão Externo", choices=ORGAOS_EXTERNOS, max_length=255, null=True, blank=True)


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
    SITUACAO_CSO = "completo"
    SITUACAO_CCO = "completo com ocorrencia"
    SITUACAO_CADASTRO = [
        (SITUACAO_INCOMPLETO, "Incompleto"),
        (SITUACAO_CSO, "Completo sem Ocorrência"),
        (SITUACAO_CCO, "Completo com Ocorrência"),
    ]
    NATUREZA_OPERACAO = [
        ("Ações de inteligência", "Ações de inteligência"),
        ("Cumprimento de Medidas Cautelares Judiciais", "Cumprimento de Medidas Cautelares Judiciais"),
        ("Apoio operacional a outras instituições", "Apoio operacional a outras instituições"),
        ("Prestação de auxílio e assistência em emergências", "Prestação de auxílio e assistência em emergências"),
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
    matricula_id_delegado_operacao = models.CharField("Matrícula/ID Funcional do Delegado", max_length=32, null=True,
                                                      blank=True)
    natureza_operacao = models.CharField(
        "Natureza da operação",
        choices=NATUREZA_OPERACAO,
        max_length=255,
        null=True
    )
    unidade_responsavel = models.CharField("Unidade da polícia judiciária responsável", choices=UNIDADES_POLICIA,
                                           max_length=255, null=True, blank=True)
    apoio_recebido = models.BooleanField(
        "Recebeu apoio de outras unidades policiais?",
        default=False
    )
    unidades_apoiadoras = models.ManyToManyField(UnidadesApoiadores)
    operacao_integrada = models.BooleanField(
        "Operação integrada com órgãos externos à Polícia Civil?",
        default=False
    )
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
    justificativa_uso_aeronave = models.TextField("Justificativa do uso de aeronave", null=True, blank=True)
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
    # numero_mortes_interv_estado = models.PositiveIntegerField(
    #     "Número de mortes por intervenção de agentes do Estado",
    #     default=0,
    #     blank=True
    # )
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
    # numero_civis_mortos_npap = models.PositiveIntegerField(
    #     "Número de civis mortos – morte não provocada por agente policiais",
    #     default=0,
    #     blank=True
    # )
    numero_veiculos_recuperados = models.PositiveIntegerField(
        "Número de veículos recuperados",
        default=0,
        blank=True
    )

    ### Info Resultados Two
    # houve_apreensao_drogas = models.BooleanField(
    #     "Houve apreensão de Drogas?",
    #     null=True,
    #     blank=True,
    # )
    droga_cocaina = models.BooleanField("Apreensão de Cocaína?", default=False)
    droga_cannabis = models.BooleanField("Apreensão de Cannabis?", default=False)
    droga_haxixe = models.BooleanField("Apreensão de Haxixe?", default=False)
    droga_sinteticos = models.BooleanField("Apreensão de Sintéticos?", default=False)
    droga_outros = models.BooleanField("Apreensão de Outros?", default=False)
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
            # self.notify_completion()

        self.situacao = self.SITUACAO_CSO
        # if self.houve_ocorrencia_operacao is True:
        #     self.situacao = self.SITUACAO_CCO

        self.save()

    def notify_completion(self):
        if self.completo is False:
            raise OperationNotCompleteException

        if not settings.DEBUG:
            notifica_por_email(self)
