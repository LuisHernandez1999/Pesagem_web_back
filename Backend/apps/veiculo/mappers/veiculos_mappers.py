from django.db import connection
from apps.veiculo.utils.veiculos_utils import cursor_sql_veiculo, search_sql_veiculo, order_sql_veiculo
from apps.veiculo.dto.veiculo_dto import CreateVeiculoDTO,VeiculoListDTO
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
            Where
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



class RankingVeiculosPesagemMapper:
    @staticmethod
    def get(
        prefixo,
        pa,
        tipo_servico,
        tipo_veiculo,
        equipamento,
        search,
        cursor,
        ordering,
        limit,
        dto: VeiculoListDTO
    ):
        search_clause, search_params = search_sql_veiculo(search)
        cursor_clause, cursor_params = cursor_sql_veiculo(cursor)
        ordering_clause = order_sql_veiculo(ordering)

        sql = f"""
        SELECT
            ranking,
            veiculo,
            total_pesagens,
            eficiencia_percentual
        FROM (
            SELECT
                ROW_NUMBER() OVER (
                    ORDER BY COUNT(p.id) DESC, p.prefixo ASC
                ) AS ranking,
                p.prefixo AS veiculo,
                COUNT(p.id) AS total_pesagens,
                ROUND(
                    (COUNT(p.id) * 100.0) /
                    NULLIF(SUM(COUNT(p.id)) OVER (), 0),
                    2
                ) AS eficiencia_percentual
            FROM pesagem p
            WHERE 1=1
            {search_clause}
            {cursor_clause}
        """

        if getattr(dto, "prefixo", None):
            sql += " AND v.prefixo = %s"
            params.append(dto.prefixo)

        params = [
            *search_params,
            *cursor_params,
        ]

       
        if prefixo:
            sql += " AND p.prefixo = %s"
            params.append(prefixo)

        if pa:
            sql += " AND v.pa = %s"
            params.append(pa)

        if tipo_servico:
            sql += " AND p.tipo_servico = %s"
            params.append(tipo_servico)

        if tipo_veiculo:
            sql += " AND v.tipo_veiculo = %s"
            params.append(tipo_veiculo)

        if equipamento:
            sql += " AND v.equipamento = %s"
            params.append(equipamento)

        sql += f"""
            GROUP BY p.prefixo
        ) ranked
        ORDER BY {ordering_clause}
        LIMIT %s
        """

        params.append(limit)

        with connection.cursor() as db:
            db.execute(sql, params)
            rows = db.fetchall()
            columns = [col[0] for col in db.description]

        return [dict(zip(columns, row)) for row in rows]



