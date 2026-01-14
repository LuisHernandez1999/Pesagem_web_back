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
