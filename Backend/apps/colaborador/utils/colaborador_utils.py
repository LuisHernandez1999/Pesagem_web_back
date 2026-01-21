from django.db import connection
from apps.colaborador.exceptions.colaborador_exceptions import (
    FuncaoInvalida,
    TurnoInvalido,
    StatusInvalido,
    PaInvalido,
)
##### sql aulixar para camada mapper 
def filtro_funcao_turno_sql(funcao, turno,pa):
    clauses = []
    params = []

    if funcao:
        clauses.append("AND funcao = %s")
        params.append(funcao)

    if turno:
        clauses.append("AND turno = %s")
        params.append(turno)
    if pa:
        clauses.append("AND pa = %s")
        params.append(pa)

    return " ".join(clauses), params

def fetch_one(sql: str, params: tuple):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()
    
###### lista para func util de tratamento de validacoes
FUNCOES_VALIDAS = {"MOTORISTA", "OPERADOR", "COLETOR"}
TURNOS_VALIDOS = {"DIURNO", "NOTURNO", "VESPERTINO"}
STATUS_VALIDOS = {"ATIVO", "INATIVO"}
PAS_VALIDOS = {"PA1", "PA2", "PA3", "PA4"}

#### protecao de order by contra sql injection
ALLOWED_ORDER_FIELDS = {"turno", "funcao"} #### lista de ordenacao pra evitar slq injection 

####### funcs validadoras
def validar_colaborador(dto):
    if dto.funcao not in FUNCOES_VALIDAS:
        raise FuncaoInvalida()

    if dto.turno not in TURNOS_VALIDOS:
        raise TurnoInvalido()

    if dto.status not in STATUS_VALIDOS:
        raise StatusInvalido()

    if dto.pa not in PAS_VALIDOS:
        raise PaInvalido()


def order_sql_colaborador(ordering: str):
    allowed = {
        "id": "id ASC",
        "-id": "id DESC",
        "nome": "nome ASC",
        "-nome": "nome DESC",
        "turno": "turno ASC",
        "-turno": "turno DESC",
        "funcao": "funcao ASC",
        "-funcao": "funcao DESC",
    }

    return allowed.get(ordering, "id DESC")
