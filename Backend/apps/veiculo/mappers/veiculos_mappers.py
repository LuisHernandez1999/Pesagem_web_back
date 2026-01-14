from django.db import connection
from apps.veiculo.utils.veiculos_utils import cursor_sql_veiculo, search_sql_veiculo, order_sql_veiculo
from apps.veiculo.dto.veiculo_dto import CreateVeiculoDTO
from apps.veiculo.utils.veiculos_utils import fetch_one

class VeiculoMapperCreate:
    ### validacao de prefixo
    @staticmethod
    def exists_by_prefixo(prefixo: str) -> bool:
        sql = "SELECT 1 FROM veiculo WHERE prefixo = %s LIMIT 1"
        return fetch_one(sql, (prefixo,)) is not None
    #### validacoao  de placa
    @staticmethod
    def exists_by_placa(placa: str | None) -> bool:
        if not placa:
            return False
        sql = "SELECT 1 FROM veiculo WHERE placa_veiculo = %s LIMIT 1"
        return fetch_one(sql, (placa,)) is not None
    #### metodo create 
    @staticmethod
    def insert(dto: CreateVeiculoDTO) -> int:
        sql = """
            INSERT INTO veiculo (
                prefixo, tipo, placa_veiculo,
                em_manutencao, tipo_servico, equipamento
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        row = fetch_one(sql, (
            dto.prefixo,
            dto.tipo,
            dto.placa_veiculo,
            dto.em_manutencao,
            dto.tipo_servico,
            dto.equipamento,
        ))
        return row[0]
    
    
###### listar veicluos
class VeiculoMapperList:
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
    
    
###### listar veicluos por tipo
class VeiculosMapperTipo:
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


