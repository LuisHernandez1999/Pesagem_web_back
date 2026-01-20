from django.db import connection
from apps.pesagem.exceptions.pesagem_execptions import (
    TipoPesagemInvalida,
    VolumeCargaInvalido,
)
from apps.pesagem.models.pesagem import Pesagem
from datetime import date


def buscar_prefixo_veiculo(prefixo_id: int) -> str | None:
   
    if not prefixo_id:
        return None

    sql = "SELECT prefixo FROM veiculo WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, [prefixo_id])
        row = cursor.fetchone()

    return row[0] if row else None


def buscar_nome_cooperativa(cooperativa_id: int) -> str | None:
    """
    Retorna o nome da cooperativa a partir do ID
    """
    if not cooperativa_id:
        return None

    sql = "SELECT nome FROM cooperativa WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, [cooperativa_id])
        row = cursor.fetchone()

    return row[0] if row else None


def buscar_colaborador_nome_matricula(colaborador_id: int) -> str | None:
    if not colaborador_id:
        return None

    sql = """
        SELECT nome, matricula
        FROM colaborador
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [colaborador_id])
        row = cursor.fetchone()

    if not row:
        return None

    nome, matricula = row
    return f"{nome} - {matricula}" if matricula else nome





def gerar_numero_doc_pesagem():
    hoje = date.today().strftime("%Y%m%d")

    sql = """
        SELECT COUNT(*)
        FROM pesagem
        WHERE data = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [date.today()])
        total_hoje = cursor.fetchone()[0]

    sequencial = total_hoje + 1

    return f"{hoje}-{sequencial:04d}"

def order_sql_pesagem(ordering: str) -> str:
    allowed = {
        "id": "p.id DESC",
        "data": "p.data DESC",
        "-data": "p.data ASC",
        "peso": "p.peso_calculado DESC",
    }
    return allowed.get(ordering, "p.id DESC")




def calcular_peso(prefixo_id: int, volume_carga: str) -> float:
    sql = "SELECT tipo FROM veiculo WHERE id = %s"
    with connection.cursor() as cursor:
        cursor.execute(sql, (prefixo_id,))
        row = cursor.fetchone()

    if not row:
        return 0
    tipo_veiculo = row[0]
    return Pesagem.VOLUMES_CARGA.get(tipo_veiculo, {}).get(volume_carga, 0)


def validar_pesagem(dto):
    tipos_validos = {x[0] for x in Pesagem.TIPOS_PESAGEM}

    if dto.tipo_pesagem not in tipos_validos:
        raise TipoPesagemInvalida()

    if not dto.volume_carga:
        raise VolumeCargaInvalido()



