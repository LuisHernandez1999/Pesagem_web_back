from django.db import connection
from apps.pesagem.utils.veiculo_utils import cursor_sql_veiculo, search_sql_veiculo, order_sql_veiculo


class VeiculoMapper:
###### listar veicluos
    @staticmethod
    def listar(cursor, limit, search, ordering):
        search_clause, search_params = search_sql_veiculo(search)
        cursor_clause, cursor_params = cursor_sql_veiculo(cursor)
        ordering_clause = order_sql_veiculo(ordering)
        sql = f"""
            SELECT
                id,
                prefixo,
                tipo,
                placa_veiculo,
                em_manutencao,
                tipo_servico,
                equipamento
            FROM veiculo
            WHERE 1=1
            {search_clause}
            {cursor_clause}
            ORDER BY {ordering_clause}, id DESC
            LIMIT %s
        """

        params = [
            *search_params,
            *cursor_params,
            limit,
        ]
        with connection.cursor() as db:
            db.execute(sql, params)
            rows = db.fetchall()

        columns = (
            "id",
            "prefixo",
            "tipo",
            "placa_veiculo",
            "em_manutencao",
            "tipo_servico",
            "equipamento",
        )

        return [dict(zip(columns, row)) for row in rows]

######### listar por tipo 
    @staticmethod
    def contagem_por_tipo(tipo_servico: str):
        sql = """
            SELECT
                COUNT(*) FILTER (WHERE tipo_servico ILIKE %s),
                COUNT(*) FILTER (
                    WHERE tipo_servico ILIKE %s
                    AND em_manutencao IN ('NÃO','Não')
                ),
                COUNT(*) FILTER (
                    WHERE tipo_servico ILIKE %s
                    AND em_manutencao IN ('SIM','Sim')
                )
            FROM veiculo
        """

        with connection.cursor() as db:
            db.execute(sql, [f"%{tipo_servico}%"] * 3)
            return db.fetchone()
