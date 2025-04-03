SELECT
op.identificador,
op.id,
op.criado_em AS "Criado em",
op.situacao AS "Situação Cadastro",

-- Informações do Registro
op.nome_operacao AS "Nome da operação",
op.tipo_operacao AS "Tipo de operação",
op.numero_inquerito_mae AS "Número do Inquérito Policial mãe",
op.numero_tjrj AS "Número do procedimento (TJRJ)",


-- Informações Gerais
TO_CHAR(op.data, 'DD/MM/YYYY') AS "Data da operação",
TO_CHAR(op.hora_inicio, 'HH24:MI') AS "Hora de início da operação",
TO_CHAR(op.hora_termino, 'HH24:MI') AS "Hora de término da operação",

    -- localidade
lo.municipio as "Município", 
lo.bairro as "Bairro", 
lo.endereco_referencia as "Endereço de referência",
lo.localidade as "Localidade", 

op.objetivo_estrategico_operacao AS "Objetivo estratégico da operação",
op.justificativa_excepcionalidade_operacao AS "Justificativa da excepcionalidade da operação",


-- Informações Operacionais
op.nome_delegado_operacao AS "Nome do Delegado Responsável",
op.matricula_id_delegado_operacao AS "Matrícula/ID Funcional do Delegado",
op.natureza_operacao AS "Natureza da operação",
op.unidade_responsavel AS "Unidade da polícia judiciária responsável (UPAJ)",
op.apoio_recebido AS "Recebeu apoio de outras unidades policiais?",

--unidades_apoiadoras 
ua.nome_unidade AS "Unidades Apoiadoras",
op.operacao_integrada AS "Operação integrada com órgãos externos?",
--orgaos_externos
oe.nome_orgao AS "Órgãos Externos",

-- Recursos Mobilizados

op.numero_agentes_mobilizados AS "Número de agentes mobilizados",
op.numero_viaturas_mobilizadas AS "Número de viaturas mobilizadas",
op.numero_veiculos_blindados AS "Número de veículos blindados",
op.numero_aeronaves AS "Número de aeronaves",
op.numero_equipes_medicas AS "Número de equipes médicas de apoio",
op.numero_ambulancia AS "Número de ambulâncias",
op.justificativa_uso_aeronave AS "Justificativa do uso de aeronave",


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
ro.numero_ro AS "Registro de ocorrência apensado",
op.houve_confronto_daf AS "Houve confronto com DAF?",
op.houve_resultados_operacao AS "Houve resultados na operação?",
op.houve_entrada_forcada AS "Houve entrada forçada em domicílio em período noturno?",
op.justificativa_entrada_forcada AS "Justificativa para entrada forçada",

--operations_roapensado
-- Presos e Feridos 
op.numero_presos_elencados AS "Presos indicados nos mandados de prisão alvo da operação?",
op.numero_presos_outros_mandados AS "Presos indicados em outros mandados de prisão pendentes?",
op.numero_presos_flagrante AS "Flagrantes? (APF lavrados)",
op.numero_adolescentes_apreendidos AS "Número de adolescentes apreendidos?",

-- Feridos, Mortos e recuperados
op.numero_policiais_feridos AS "Número de policiais feridos?",
op.numero_mortes_policiais AS "Número de mortes policiais?",
op.numero_civis_mortos AS "Número de civis mortos?",
op.numero_civis_feridos AS "Número de civis feridos?",
op.numero_veiculos_recuperados AS "Número de veículos recuperados?",

-- Apreensões

op.droga_cocaina AS "Apreensão de Cocaína",
op.droga_cannabis AS "Apreensão de Cannabis",
op.droga_haxixe AS "Apreensão de Haxixe",
op.droga_sinteticos AS "Apreensão de Sintéticos",
op.droga_outros AS "Apreensão de Outros",
op.numero_explosivos_apreendidos AS "Artefatos explosivos apreendidos?",
op.numero_armas_apreendidas AS "Armas apreendidas?",
op.numero_fuzis_apreendidos AS "Do total de armas, quantos fuzis?",
op.numero_carregadores_apreendidos AS "Carregadores apreendidos?",
op.numero_municoes_apreendidas AS "Munições apreendidas?",

--operations_cartuchocalibresapreendidos
cc.tipo_cartucho as "Cartucho",
cc.tipo_calibre AS "Calibre",

-- Registros e Perícias
op.houve_disparados_aeronave AS "Houve disparos embarcado da aeronave?",
op.houve_registros_imagem AS "Foram feitos registros de imagem a partir da aeronave?",
op.local_preservado AS "O local foi preservado?",

op.pericia_local AS "Foi feita perícia no local?",
op.pericia_aeronave AS "Foi feita perícia na aeronave?",
op.pericia_veiculo_blindado AS "Foi feita perícia no veículo blindado?",
op.pericia_viaturas AS "Foi feita perícia nas viaturas?",
op.pericia_iml AS "Foi feita perícia no IML?",
op.pericia_outras AS "Foram feitas outras perícias?",

-- Observações
op.observacoes_gerais AS "Observações gerais"

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
WHERE op.identificador = %s