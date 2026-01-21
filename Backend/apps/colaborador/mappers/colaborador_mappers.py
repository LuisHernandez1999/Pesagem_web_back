from apps.colaborador.dto.colaborador_dto import CreateColaboradorDTO,ColaboradorListDTO,ColaboradorListItemDTO
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
    def listar(dto: ColaboradorListDTO):
        filtro_sql, filtro_params = filtro_funcao_turno_sql(
            dto.funcao,
            dto.turno,
            dto.pa,
        )

        ordering_clause = order_sql_colaborador(dto.ordering)

        cursor_sql = ""
        cursor_params = []
        if dto.cursor:
            cursor_sql = "AND c.id < %s"
            cursor_params.append(dto.cursor)

        sql = f"""
            SELECT
                c.id,
                c.nome,
                c.matricula,
                c.funcao,
                c.turno,
                c.status,
                c.pa
            FROM colaborador c
            WHERE 1=1
            {filtro_sql}
            {cursor_sql}
            ORDER BY {ordering_clause}, c.id DESC
            LIMIT %s
        """

        params = [
            *filtro_params,
            *cursor_params,
            dto.limit,
        ]

        with connection.cursor() as db:
            db.execute(sql, params)
            rows = db.fetchall()

        columns = (
            "id", "nome", "matricula",
            "funcao", "turno", "status", "pa"
        )

        return [
            ColaboradorListItemDTO(
                id=row[0],
                nome=row[1],
                matricula=row[2],
                funcao=row[3],
                turno=row[4],
                status=row[5],
                pa=row[6],
            )
            for row in rows
        ]