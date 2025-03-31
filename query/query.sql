SELECT
    op.id,
    op.criado_em AS "Criado em",
    op.secao_atual AS "Seção Atual",
    op.completo AS "Cadastro Completo",
    op.situacao AS "Situação Cadastro",
    op.registro_anterior AS "Dado registrado fora do sistema",

    -- Informações do Registro
    op.numero_inquerito_mae AS "Número do Inquérito Policial mãe",
    op.numero_tjrj AS "Número do procedimento (TJRJ)",
    op.tipo_operacao AS "Tipo de operação",
    op.nome_operacao AS "Nome da operação",

    -- Informações Gerais
    op.data AS "Data",
    op.hora_inicio AS "Hora de início da operação",
    op.hora_termino AS "Hora de término da operação",

    op.justificativa_excepcionalidade_operacao AS "Justificativa da excepcionalidade da operação",
    op.objetivo_estrategico_operacao AS "Objetivo estratégico da operação",

    -- Informações Operacionais
    op.nome_delegado_operacao AS "Nome do Delegado Responsável",
    op.matricula_id_delegado_operacao AS "Matrícula/ID Funcional do Delegado",
    op.natureza_operacao AS "Natureza da operação",
    op.unidade_responsavel AS "Unidade da polícia judiciária responsável",
    op.apoio_recebido AS "Recebeu apoio de outras unidades policiais?",
    op.operacao_integrada AS "Operação integrada com órgãos externos?",

    -- Recursos Mobilizados
    op.numero_viaturas_mobilizadas AS "Número de viaturas mobilizadas",
    op.numero_agentes_mobilizados AS "Número de agentes mobilizados",
    op.numero_veiculos_blindados AS "Número de veículos blindados",
    op.numero_aeronaves AS "Número de aeronaves",
    op.numero_ambulancia AS "Número de ambulâncias",
    op.justificativa_uso_aeronave AS "Justificativa do uso de aeronave",
    op.numero_equipes_medicas AS "Número de equipes médicas de apoio",

    -- Comunicação e Risco
    op.escolas_perto AS "Escolas nas proximidades?",
    op.comunicacao_escola AS "Houve comunicação prévia às autoridades de educação?",
    op.justificativa_omissao_comunicacao_escola AS "Justificativa para omissão da comunicação às autoridades de educação",
    op.orgao_autoridade_comunicacao_escola AS "Órgãos ou autoridades alertados",
    op.canal_comunicacao_escola AS "Canal de comunicação utilizado",

    op.saude_perto AS "Unidades de saúde nas proximidades?",
    op.comunicacao_saude AS "Houve comunicação prévia às autoridades de saúde?",
    op.justificativa_omissao_comunicacao_saude AS "Justificativa para omissão da comunicação às autoridades de saúde",
    op.orgao_autoridade_comunicacao_saude AS "Órgãos ou autoridades alertados",
    op.canal_comunicacao_saude AS "Canal de comunicação utilizado",

    op.descricao_analise_risco AS "Análise de riscos e medidas de controle",

    -- Resultados da Operação
    op.houve_confronto_daf AS "Houve confronto com DAF?",
    op.houve_resultados_operacao AS "Houve resultados na operação?",
    op.houve_entrada_forcada AS "Houve entrada forçada em domicílio?",
    op.justificativa_entrada_forcada AS "Justificativa para entrada forçada",

    -- Presos e Feridos
    op.numero_presos_elencados AS "Número de presos elencados",
    op.numero_presos_outros_mandados AS "Número de presos em outros mandados",
    op.numero_presos_flagrante AS "Número de presos em flagrante",
    op.numero_adolescentes_apreendidos AS "Número de adolescentes apreendidos",

    -- Feridos e Mortos
    op.numero_policiais_feridos AS "Número de policiais feridos",
    op.numero_mortes_policiais AS "Número de mortes policiais",
    op.numero_civis_mortos AS "Número de civis mortos",
    op.numero_civis_feridos AS "Número de civis feridos",

    -- Apreensões
    op.numero_veiculos_recuperados AS "Número de veículos recuperados",
    op.droga_cocaina AS "Apreensão de Cocaína",
    op.droga_cannabis AS "Apreensão de Cannabis",
    op.droga_haxixe AS "Apreensão de Haxixe",
    op.droga_sinteticos AS "Apreensão de Sintéticos",
    op.droga_outros AS "Apreensão de Outros",
    op.numero_explosivos_apreendidos AS "Número de explosivos apreendidos",
    op.numero_armas_apreendidas AS "Número de armas apreendidas",
    op.numero_fuzis_apreendidos AS "Número de fuzis apreendidos",
    op.numero_carregadores_apreendidos AS "Número de carregadores apreendidos",
    op.numero_municoes_apreendidas AS "Número de munições apreendidas",

    -- Registros e Perícias
    op.houve_disparados_aeronave AS "Houve disparos embarcados da aeronave?",
    op.houve_registros_imagem AS "Registros de imagem da aeronave?",
    op.local_preservado AS "Local permaneceu preservado?",
    op.pericia_local AS "Foi feita perícia no local?",
    op.pericia_aeronave AS "Foi feita perícia na aeronave?",
    op.pericia_veiculo_blindado AS "Foi feita perícia no veículo blindado?",
    op.pericia_viaturas AS "Foi feita perícia nas viaturas?",
    op.pericia_iml AS "Foi feita perícia no IML?",
    op.pericia_outras AS "Foram feitas outras perícias?",

    -- Observações
    op.observacoes_gerais AS "Observações gerais",

    -- localidade
    lo.localidade as "Localidade", 
    lo.municipio as "Município", 
    lo.bairro as "Bairro", 
    lo.endereco_referencia as "Endereço de referência",
    
	--unidades_apoiadoras 
    ua.nome_unidade AS "Unidades Apoiadoras",
    
    --orgaos_externos
    oe.nome_orgao AS "Órgãos Externos",
    
    --operations_roapensado
    ro.numero_ro AS "Registro de Ocorrência",
    
    --operations_cartuchocalibresapreendidos
    cc.tipo_calibre AS "Calibres Apreendidos",
    cc.tipo_cartucho as "Cartuchos Apreendidos"
    
FROM operacao op
-- Join para LocalidadeOperacao
LEFT JOIN operacao_localidade_operacao ol ON op.id = ol.operacao_id
LEFT JOIN operations_localidadeoperacao lo ON ol.localidadeoperacao_id = lo.id
-- Join para UnidadesApoiadoras
LEFT JOIN operacao_unidades_apoiadoras ou ON op.id = ou.operacao_id
LEFT JOIN operations_unidadesapoiadores ua ON ou.unidadesapoiadores_id = ua.id
-- Join para OrgaosExternosOperacao
LEFT JOIN operacao_orgaos_externos oo ON op.id = oo.operacao_id
LEFT JOIN operations_orgaosexternosoperacao oe ON oo.orgaosexternosoperacao_id = oe.id
-- Join para ROApensado (Registro de Ocorrência)
LEFT JOIN operacao_registro_ocorrencia orc ON op.id = orc.operacao_id
LEFT JOIN operations_roapensado ro ON orc.roapensado_id = ro.id
-- Join para CartuchosCalibresApreendidos
LEFT JOIN operacao_cartuchos_calibres oc ON op.id = oc.operacao_id
LEFT JOIN operations_cartuchocalibresapreendidos cc ON oc.cartuchocalibresapreendidos_id = cc.id
WHERE op.identificador = %s;
