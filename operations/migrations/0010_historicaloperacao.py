# Generated by Django 3.1.6 on 2021-03-12 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operations', '0009_remove_operacao_editado'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalOperacao',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('completo', models.BooleanField(default=False, verbose_name='Cadastro Completo')),
                ('situacao', models.CharField(choices=[('incompleto', 'Incompleto'), ('completo sem ocorrencia', 'Completo sem Ocorrência'), ('completo com ocorrencia', 'Completo com Ocorrência')], default='incompleto', max_length=100, verbose_name='Situação Cadastro')),
                ('identificador', models.UUIDField(db_index=True, editable=False)),
                ('criado_em', models.DateTimeField(blank=True, editable=False, verbose_name='Criado em')),
                ('data', models.DateField(blank=True, null=True, verbose_name='Data')),
                ('hora', models.TimeField(blank=True, null=True, verbose_name='Hora')),
                ('localidade', models.CharField(blank=True, max_length=255, null=True, verbose_name='Localidade')),
                ('municipio', models.CharField(blank=True, max_length=255, null=True, verbose_name='Município')),
                ('bairro', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bairro')),
                ('endereco_referencia', models.CharField(blank=True, max_length=255, null=True, verbose_name='Endereço de referência')),
                ('coordenadas_geo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Referência geográfica')),
                ('batalhao_responsavel', models.CharField(blank=True, max_length=255, null=True, verbose_name='Batalhão Responsável')),
                ('justificativa_excepcionalidade_operacao', models.TextField(blank=True, null=True, verbose_name='Justificativa da excepcionalidade da operação')),
                ('descricao_analise_risco', models.TextField(blank=True, null=True, verbose_name='Análise de riscos e medidas de controles de danos colaterais das operações e de disparos de confrontos')),
                ('unidade_responsavel', models.CharField(blank=True, max_length=255, null=True, verbose_name='Unidade operacional responsável')),
                ('unidade_apoiadora', models.CharField(blank=True, max_length=255, null=True, verbose_name='Unidade Apoiadora')),
                ('nome_comandante_operacao', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do Comandante')),
                ('rg_pm_comandante_operacao', models.CharField(blank=True, max_length=10, null=True, verbose_name='RG PM do Comandante')),
                ('posto_comandante_operacao', models.CharField(choices=[('Cel', 'Coronel'), ('Ten Cel', 'Tenente Coronel'), ('Maj', 'Major'), ('Cap', 'Capitão'), ('1 Ten', 'Primeiro Tenente'), ('2 Ten', 'Segundo Tenente'), ('Subten', 'Subtenente'), ('1 Sgt', 'Primeiro Sargento'), ('2 Sgt', 'Segundo Sargento'), ('3 Sgt', 'Terceiro Sargento'), ('Cb', 'Cabo'), ('Sd', 'Soldado')], max_length=100, null=True, verbose_name='Posto|Graduação do Comandante')),
                ('tipo_operacao', models.CharField(choices=[('Pl', 'Planejada'), ('Em', 'Emergencial')], max_length=10, null=True, verbose_name='Tipo de operação')),
                ('tipo_acao_repressiva', models.CharField(choices=[('AREP I', 'AREP I'), ('AREP II', 'AREP II'), ('AREP III', 'AREP III'), ('AREP IV', 'AREP IV')], max_length=15, null=True, verbose_name='Tipo de ação repressiva')),
                ('numero_ordem_operacoes', models.CharField(blank=True, max_length=100, null=True, verbose_name='Número da ordem de operações no caso de operação planejada')),
                ('objetivo_estrategico_operacao', models.CharField(blank=True, max_length=255, null=True, verbose_name='Objetivo estratégico da operação')),
                ('numero_guarnicoes_mobilizadas', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de Guarnições mobilizadas')),
                ('numero_policiais_mobilizados', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de policiais mobilizados')),
                ('numero_veiculos_blindados', models.PositiveIntegerField(blank=True, default=0, verbose_name='Número de veículos blindados')),
                ('numero_aeronaves', models.PositiveIntegerField(blank=True, default=0, verbose_name='Número de aeronaves')),
                ('houve_confronto_daf', models.BooleanField(blank=True, null=True, verbose_name='Houve confronto com DAF?')),
                ('houve_resultados_operacao', models.BooleanField(blank=True, null=True, verbose_name='Houve resultados na operação?')),
                ('houve_ocorrencia_operacao', models.BooleanField(blank=True, null=True, verbose_name='Houve ocorrência na operação?')),
                ('boletim_ocorrencia_pm', models.CharField(blank=True, max_length=100, null=True, verbose_name='Boletim de Ocorrência da Polícia Militar (BOPM)')),
                ('registro_ocorrencia', models.CharField(blank=True, max_length=100, null=True, verbose_name='Registro de Ocorrência')),
                ('nome_comandante_ocorrencia', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome do Comandante')),
                ('rg_pm_comandante_ocorrencia', models.CharField(blank=True, max_length=100, null=True, verbose_name='RG PM do Comandante')),
                ('posto_comandante_ocorrencia', models.CharField(choices=[('Cel', 'Coronel'), ('Ten Cel', 'Tenente Coronel'), ('Maj', 'Major'), ('Cap', 'Capitão'), ('1 Ten', 'Primeiro Tenente'), ('2 Ten', 'Segundo Tenente'), ('Subten', 'Subtenente'), ('1 Sgt', 'Primeiro Sargento'), ('2 Sgt', 'Segundo Sargento'), ('3 Sgt', 'Terceiro Sargento'), ('Cb', 'Cabo'), ('Sd', 'Soldado')], max_length=100, null=True, verbose_name='Posto|Graduação do Comandante')),
                ('houve_apreensao_drogas', models.BooleanField(blank=True, null=True, verbose_name='Houve apreensão de Drogas?')),
                ('numero_armas_apreendidas', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de armas apreendidas')),
                ('numero_fuzis_apreendidos', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de fuzis apreendidos')),
                ('numero_presos', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número presos')),
                ('numero_adolescentes_apreendidos', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de adolescentes apreendidos')),
                ('numero_policiais_feridos', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de policiais feridos')),
                ('numero_mortes_policiais', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de mortes policiais')),
                ('numero_mortes_interv_estado', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de mortes por intervenção de agentes do Estado')),
                ('numero_civis_feridos', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de civis feridos')),
                ('numero_civis_mortos_npap', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de civis mortos – morte não provocada por agente policiais')),
                ('numero_veiculos_recuperados', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de veículos recuperados')),
                ('observations', models.TextField(blank=True, null=True, verbose_name='Observações gerais')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Histórico de alterações da operação',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
