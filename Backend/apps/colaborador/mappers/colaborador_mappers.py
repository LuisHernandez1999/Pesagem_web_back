from apps.colaborador.dto.colaborador_dto import CreateColaboradorDTO
from apps.colaborador.utils.colaborador_utils import fetch_one
from django.db import connection
from apps.colaborador.utils.colaborador_utils import filtro_funcao_turno_sql,order_sql_colaborador


class ColaboradorMapperCreate:
    @staticmethod
    def exists_by_matricula(matricula: int) -> bool:
        sql = "SELECT 1 FROM colaborador WHERE matricula = %s LIMIT 1"
        return fetch_one(sql, (matricula,)) is not None
    @staticmethod
    def insert(dto: CreateColaboradorDTO) -> int:
        sql = """
            INSERT INTO colaborador (
                nome, matricula, funcao,
                turno, status, pa
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        row = fetch_one(sql, (
            dto.nome,
            dto.matricula,
            dto.funcao,
            dto.turno,
            dto.status,
            dto.pa,
        ))
        return row[0]
    
class ColaboradorMapperList:
    @staticmethod
    def listar(cursor, limit, funcao, turno,ordering):
        filtro_sql, filtro_params = filtro_funcao_turno_sql(funcao, turno)
        ordering_clause = order_sql_colaborador(ordering)
        cursor_sql = ""
        cursor_params = []
        if cursor:
            cursor_sql = "AND id < %s"
            cursor_params.append(cursor)

        sql = f"""
            SELECT
                id,
                nome,
                matricula,
                funcao,
                turno,
                status,
                pa
            FROM colaborador
            WHERE 1=1
            {filtro_sql}
            {cursor_sql}
            ORDER BY {ordering_clause}, id DESC
            LIMIT %s
        """

        params = [
            *filtro_params,
            *cursor_params,
            limit,
        ]

        with connection.cursor() as db:
            db.execute(sql, params)
            rows = db.fetchall()

        columns = (
            "id",
            "nome",
            "matricula",
            "funcao",
            "turno",
            "status",
            "pa",
        )

        return [dict(zip(columns, row)) for row in rows]