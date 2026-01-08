def cursor_sql_veiculo(cursor: int | None) -> tuple[str, list]:
    if not cursor:
        return "", []
    return "AND id < %s", [cursor]


def search_sql_veiculo(search: str | None) -> tuple[str, list]:
    if not search:
        return "", []
    return "AND prefixo ILIKE %s", [f"%{search}%"]


def order_sql_veiculo(ordering: str) -> str:
    direction = "DESC" if ordering.startswith("-") else "ASC"
    field = ordering.lstrip("-")
    return f"{field} {direction}"
