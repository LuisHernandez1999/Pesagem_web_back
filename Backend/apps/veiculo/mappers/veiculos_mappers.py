from django.db import connection
from apps.veiculo.utils.veiculos_utils import cursor_sql_veiculo, search_sql_veiculo, order_sql_veiculo
from apps.veiculo.dto.veiculo_dto import VeiculoDTO,VeiculoListDTO,VeiculoRankingDTO
from apps.veiculo.utils.veiculos_utils import fetch_one

class VeiculoMapperCreate:
    ### validacao de prefixo
    @staticmethod
    def exists_by_prefixo(prefixo: str) -> bool:
        sql = "SELECT 1 FROM veiculo WHERE prefixo = %s LIMIT 1"
        return fetch_one(sql, (prefixo,)) is not None
    #### validacoao  de placa
    @staticmethod
    def exists_by_placa(placa_veiculo: str | None) -> bool:
        if not placa_veiculo:
            return False
        sql = "SELECT 1 FROM veiculo WHERE placa_veiculo = %s LIMIT 1"
        return fetch_one(sql, (placa_veiculo,)) is not None
    #### metodo create 
    @staticmethod
    def insert(dto: VeiculoDTO) -> int:
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
            dto.tipo_veiculo,
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
        ordering_clause = order_sql_veiculo(ordering) or "id"

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
            ORDER BY {ordering_clause} DESC, id DESC
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



class RankingVeiculosPesagemMapper:
    @staticmethod
    def get(dto):
        search_clause, search_params = search_sql_veiculo(dto.search)
        cursor_clause, cursor_params = cursor_sql_veiculo(dto.cursor)

        sql = f"""
        SELECT
            v.prefixo AS veiculo,
            COUNT(p.id) AS total_pesagens
        FROM pesagem p
        JOIN veiculo v ON v.id = p.prefixo_id
        WHERE 1=1
        {search_clause}
        {cursor_clause}
        GROUP BY v.prefixo
        ORDER BY total_pesagens DESC, v.prefixo ASC
        LIMIT %s
        """

        params = [
            *search_params,
            *cursor_params,
            dto.limit,
        ]

        with connection.cursor() as db:
            db.execute(sql, params)
            rows = db.fetchall()

        data = [
            {"veiculo": r[0], "total_pesagens": r[1]}
            for r in rows
        ]

        total_geral = sum(i["total_pesagens"] for i in data) or 1

        for idx, item in enumerate(data, start=1):
            item["ranking"] = idx
            item["eficiencia_percentual"] = round(
                (item["total_pesagens"] * 100) / total_geral,
                2
            )

        return data


    



