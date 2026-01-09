from django.db import connection

ALLOWED_ORDER_FIELDS = {"prefixo", "tipo", "tipo_servico"} #### lista de ordenacao pra evitar slq injection 


def cursor_sql_veiculo(cursor: int | None) -> tuple[str, list]:
    if not cursor:
        return "", []
    return "AND id < %s", [cursor]


def search_sql_veiculo(search: str | None) -> tuple[str, list]:
    if not search:
        return "", []
    return "AND prefixo ILIKE %s", [f"%{search}%"]


def order_sql_veiculo(ordering: str | None):
    if ordering not in ALLOWED_ORDER_FIELDS:
        return "prefixo"
    return ordering #### ordenacao pra evitar sql injection 



def fetch_one(sql: str, params: tuple):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()


def execute(sql: str, params: tuple):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)