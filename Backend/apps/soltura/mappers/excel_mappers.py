from collections import Counter, defaultdict
from apps.soltura.utils.excel_utils import determinar_turno
from apps.soltura.models.soltura import Soltura


def map_soltura_to_row(s: Soltura, tipo_servico: str):
    col_list = list(s.coletores.all())

    motorista_fmt = ""
    if s.motorista:
        mot_nome = getattr(s.motorista, "nome", "") or ""
        mot_matricula = str(getattr(s.motorista, "matricula", "") or "")
        motorista_fmt = f"{mot_nome} - {mot_matricula}".strip().rstrip(" -")

    def fmt_col(c):
        if not c:
            return ""
        nome = getattr(c, "nome", "") or ""
        matricula = str(getattr(c, "matricula", "") or "")
        return f"{nome} - {matricula}".strip().rstrip(" -")

    coletor1 = fmt_col(col_list[0]) if len(col_list) > 0 else ""
    coletor2 = fmt_col(col_list[1]) if len(col_list) > 1 else ""
    coletor3 = fmt_col(col_list[2]) if len(col_list) > 2 else ""

    row_data = [
        s.data_soltura.strftime("%d/%m/%Y") if s.data_soltura else "",
        s.veiculo.prefixo if s.veiculo else "",
        s.hora_saida_frota.strftime("%H:%M:%S") if s.hora_saida_frota else "",
        s.lider or "",
        motorista_fmt,
        coletor1,
        coletor2,
        coletor3,
    ]

    if tipo_servico == "Remoção":
        row_data.insert(2, s.setor.nome_setor if s.setor else "")
    else:
        row_data.insert(2, getattr(getattr(s, "rota", None), "rota", "") or "")

    return row_data


def get_header(tipo_servico: str):
    header = [
        "Data",
        "Prefixo Veículo",
        "Hora Saída",
        "Líder",
        "Motorista",
        "Coletor 1",
        "Coletor 2",
        "Coletor 3",
    ]

    if tipo_servico == "Remoção":
        header.insert(2, "Setor")
    else:
        header.insert(2, "Rota")

    return header


def get_especifico_nome(s: Soltura, campo_especifico: str):
    if campo_especifico == "setor":
        return getattr(getattr(s, "setor", None), "nome_setor", None) or "Sem Setor"
    return getattr(getattr(s, "rota", None), "rota", None) or "Sem Rota"


class SolturaReportProcessMapper:

    @classmethod
    def process(cls, qs, tipo_servico, campo_especifico):
        dados_por_dia_turno = defaultdict(lambda: defaultdict(int))
        dados_por_pa = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        garagem_counter = Counter()
        lider_counter = Counter()
        especifico_counter = Counter()

        rows = []

        for s in qs:
            rows.append(map_soltura_to_row(s, tipo_servico))

            pa = s.garagem or "Sem Garagem"

            if s.data_soltura and s.hora_saida_frota:
                turno = determinar_turno(s.hora_saida_frota)
                dados_por_dia_turno[s.data_soltura][turno] += 1
                dados_por_pa[pa][s.data_soltura][turno] += 1

            garagem_counter[pa] += 1
            lider_counter[s.lider or "Sem Líder"] += 1
            especifico_counter[get_especifico_nome(s, campo_especifico)] += 1

        return {
            "total_registros": len(rows),
            "dados_por_dia_turno": dict(dados_por_dia_turno),
            "dados_por_pa": dict(dados_por_pa),
            "garagem_counter": garagem_counter,
            "lider_counter": lider_counter,
            "especifico_counter": especifico_counter,
            "rows": rows,
        }

