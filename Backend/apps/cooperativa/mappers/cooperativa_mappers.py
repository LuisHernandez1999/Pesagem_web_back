from django.db import connection
from apps.cooperativa.dto.cooperativa_dto import CreateCooperativaDTO


class CooperativaMapperCreate:
    @staticmethod
    def exists_by_nome(nome: str) -> bool:
        sql = "SELECT 1 FROM cooperativa WHERE nome = %s LIMIT 1"
        with connection.cursor() as cursor:
            cursor.execute(sql, [nome])
            return cursor.fetchone() is not None

    @staticmethod
    def insert(dto: CreateCooperativaDTO) -> int:
        sql = """
            INSERT INTO cooperativa (nome)
            VALUES (%s)
            RETURNING id
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [dto.nome])
            return cursor.fetchone()[0]





class CooperativaEficienciaMapper:
    @staticmethod
    def get(dto):
        sql = """
        SELECT
            ranking,
            cooperativa,
            total_pesagens,
            eficiencia_percentual
        FROM (
            SELECT
                ROW_NUMBER() OVER (
                    ORDER BY COUNT(p.id) DESC, c.nome ASC
                ) AS ranking,
                c.nome AS cooperativa,
                COUNT(p.id) AS total_pesagens,
                ROUND(
                    (COUNT(p.id) * 100.0) /
                    NULLIF(SUM(COUNT(p.id)) OVER (), 0),
                    2
                ) AS eficiencia_percentual
            FROM pesagem p
            INNER JOIN cooperativa c ON c.id = p.cooperativa_id
            WHERE 1=1
        """
        params = []

        if getattr(dto, "nome", None):
            sql += " AND c.nome = %s"
            params.append(dto.nome)

        sql += """
            GROUP BY c.id, c.nome
        ) ranked
        ORDER BY ranking
        LIMIT 15
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

        return [dict(zip(columns, row)) for row in rows]