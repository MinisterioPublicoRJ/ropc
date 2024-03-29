import csv
import re
import uuid
import unicodedata
from datetime import datetime
from hashlib import md5

import rows
import tqdm
from django.contrib.auth import get_user_model

from operations.models import Operacao


User = get_user_model()
BOPM_PATTERN = re.compile(r"\d{4,}")


def slug(val):
    return unicodedata.normalize(
        "NFKD", val.strip().lower()
    ).encode("ascii", "ignore").decode()


def parse_tipo_opercao(row):
    col_name = "tipo_de_operacao"
    val = None
    if row[col_name] == "EMERGENCIAL":
        val = "Em"
    elif row[col_name] == "PLANEJADA":
        val = "Pl"

    return val


def parse_tipo_acao_repressiva(row):
    val = row["tipo_da_acao_repressiva"].strip().lower()
    tipo = re.match(r"a rep (\d)", val)
    new_val = None
    if tipo:
        new_val = Operacao.TIPO_ACAO_REPRESSIVA[int(tipo.group(1)) - 1][0]

    return new_val


def parse_data(row):
    col_name = "dia"
    return datetime.strptime(row[col_name], "%d/%m/%Y").date()


def parse_hora(row):
    col_name = "hora"
    val = re.sub(r"\s+(PM|AM)", "", row[col_name])
    return datetime.strptime(val, "%H:%M:%S").time()


def parse_unidade_responsavel(row):
    col_names = (
        "field_1_cpa",
        "field_2_cpa",
        "field_3_cpa",
        "field_4_cpa",
        "field_5_cpa",
        "field_6_cpa",
        "field_7_cpa",
        "cpp",
        "coe",
        "cpe"
    )
    val = None
    for col in col_names:
        if row[col]:
            val = row[col]
            break

    return val


def parse_civis_feridos(row):
    return row["civis_feridos"] + row["resistencias_feridos"]


def parse_veiculos_blindados(row):
    col_name = "houve_emprego_de_viatura_blindada_de_transporte_de_pessoal"
    return 1 if slug(row[col_name]) == "sim" else 0


def parse_houve_confronto_daf(row):
    col_name = "houve_confronto_com_daf"
    return 1 if slug(row[col_name]) == "sim" else 0


def parse_houve_resultados_operacao(row):
    col_name = "houve_resultado_na_operacao"
    return 1 if slug(row[col_name]) == "sim" else 0


def parse_houve_apreesao_drogas(row):
    col_name = "houve_apreensao_de_drogas"
    return 1 if slug(row[col_name]) == "sim" else 0


def parse_situacao(row):
    match = BOPM_PATTERN.search(row["bopm"])
    situacao = Operacao.SITUACAO_CSO
    if match:
        situacao = Operacao.SITUACAO_CCO

    return situacao


def parse_final_value(val):
    p_val = val
    if val == 0:
        p_val = 0
    elif val == "":
        p_val = None

    return p_val


def translate_data(row, mapper):
    parsed_row = dict()
    for key, value in mapper.items():
        if callable(value):
            new_val = value(row)
        else:
            new_val = row[value]

        parsed_row[key] = parse_final_value(new_val)

    return parsed_row


def get_user(unidade_responsavel, emails, salt):
    user = None
    row = None
    for email in emails:
        if unidade_responsavel is not None and re.search(email.unidade, unidade_responsavel):
            username = rows.fields.slug(email.unidade)
            user_email = email.email
            user, created = User.objects.get_or_create(username=username, email=user_email)
            if created:
                password = md5((salt + user_email).encode()).hexdigest()[:10]
                user.set_password(password)
                user.save()
                row = {
                    "username": username,
                    "email": user_email,
                    "password": password,
                    "salt": salt,
                }
            break
    else:
        print(f"Email não encontrado para Unidade: {unidade_responsavel}")

    return user, row


def run(*args):
    columns_mapper = {
        "data": parse_data,
        "hora": parse_hora,
        "localidade": "local",
        "batalhao_responsavel": "apol",
        "unidade_responsavel": parse_unidade_responsavel,
        "unidade_apoiadora": "unidade_apoiadora",
        "nome_comandante_operacao": "comandante_da_operacao",
        "rg_pm_comandante_operacao": "rg",
        "posto_comandante_operacao": "posto_graduacao",
        "tipo_operacao": parse_tipo_opercao,
        "tipo_acao_repressiva": parse_tipo_acao_repressiva,
        "numero_ordem_operacoes": "ordem_de_operacoes",
        "objetivo_estrategico_operacao": "objetivo",
        "houve_confronto_daf": parse_houve_confronto_daf,
        "houve_resultados_operacao": parse_houve_resultados_operacao,
        "boletim_ocorrencia_pm": "bopm",
        "registro_ocorrencia": "ro",
        "houve_apreensao_drogas": parse_houve_apreesao_drogas,
        "numero_armas_apreendidas": "quantidade_de_armas",
        "numero_presos": "quantidade_de_presos",
        "numero_adolescentes_apreendidos": "quantidade_de_menores_apreendidos",
        "numero_policiais_feridos": "militares_feridos",
        "numero_mortes_policiais": "baixas_militares",
        "numero_mortes_interv_estado": "resistencia_mortos",
        "numero_civis_feridos": parse_civis_feridos,
        "numero_civis_mortos_npap": "baixas_civis",
        "numero_veiculos_recuperados": "quantidade_de_veiculos_recuperados",
        "numero_veiculos_blindados": parse_veiculos_blindados,
        "nome_condutor_ocorrencia": "condutor_da_ocorrencia",
        "observacoes_gerais": "tipo_da_acao_repressiva",
        "situacao": parse_situacao,
    }
    csv_filename = args[0]
    email_filename = args[1]
    salt = args[2]
    output_filename = args[3]
    table = rows.import_from_csv(
        csv_filename,
        force_types={"rg":rows.fields.TextField}
    )
    emails = rows.import_from_csv(email_filename)
    parsed_rows = []
    csv_rows = []
    for row in tqdm.tqdm(table):
        p_row = translate_data(row._asdict(), columns_mapper)
        p_row["identificador"] = uuid.uuid4()
        p_row["usuario"], csv_row = get_user(
            p_row["unidade_responsavel"],
            emails,
            salt
        )
        csv_rows.append(csv_row)
        p_row["completo"] = True
        p_row["registro_anterior"] = True
        p_row["secao_atual"] = Operacao.n_sections + 1
        if p_row["usuario"] is not None:
            parsed_rows.append(Operacao(**p_row))

    Operacao.objects.bulk_create(parsed_rows)
    with open(output_filename, "w") as fobj:
        writer = csv.DictWriter(
            fobj,
            fieldnames=["username", "email", "password", "salt"]
        )
        writer.writeheader()
        [writer.writerow(r) for r in csv_rows if r]
