from django.db import connection

from apps.veiculo.exceptions.veiculos_exceptions import (
    VeiculoAlreadyExists,
    PlacaAlreadyExists,
    InvalidPayloadException,
    TipoVeiculoInvalido,
    StatusVeiculoInvalido,
    TipoServicoInvalido,
)

# campos permitidos para ordenação (proteção contra SQL Injection)
ALLOWED_ORDER_FIELDS = {"prefixo", "tipo", "tipo_servico"}



def cursor_sql_veiculo(cursor: int | None) -> tuple[str, list]:
    if not cursor:
        return "", []
    return "AND id < %s", [cursor]


def search_sql_veiculo(search: str | None) -> tuple[str, list]:
    if not search:
        return "", []
    return "AND prefixo ILIKE %s", [f"%{search}%"]


def order_sql_veiculo(ordering: str | None) -> str:
    if ordering not in ALLOWED_ORDER_FIELDS:
        return "prefixo"
    return ordering


def fetch_one(sql: str, params: tuple):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()


def execute(sql: str, params: tuple):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)


# SQL auxiliar (mantido, mesmo sendo mais de colaborador)



def validar_veiculo(dto):
    if not dto:
        raise InvalidPayloadException()
    if not dto.prefixo:
        raise InvalidPayloadException("Prefixo é obrigatório")
    if not dto.placa_veiculo:
        raise InvalidPayloadException("Placa é obrigatória")
    sql = "SELECT 1 FROM veiculo WHERE prefixo = %s LIMIT 1"
    if fetch_one(sql, (dto.prefixo,)):
        raise VeiculoAlreadyExists()
    sql = "SELECT 1 FROM veiculo WHERE placa_veiculo = %s LIMIT 1"
    if fetch_one(sql, (dto.placa_veiculo,)):
        raise PlacaAlreadyExists()
    if not dto.tipo_veiculo:
        raise TipoVeiculoInvalido()
    if not dto.tipo_servico:
        raise TipoServicoInvalido()