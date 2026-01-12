from apps.pesagem.utils.pesagem_utils import order_sql_pesagem
from django.db import connection
from apps.pesagem.dto.pesagem_dto import CreatePesagemDTO
from apps.pesagem.utils.pesagem_utils import calcular_peso
from apps.pesagem.models import Pesagem, Colaborador, Veiculo, Cooperativa
from apps.pesagem.dto.pesagem_dto import CreatePesagemDTO

def calcular_peso(prefixo_id, volume_carga):
    if not prefixo_id or not volume_carga:
        return 0
    tipo_veiculo = prefixo_id.tipo
    return Pesagem.VOLUMES_CARGA.get(tipo_veiculo, {}).get(volume_carga, 0)


class PesagemMapperCreate:
    @staticmethod
    def insert(dto):
        pesagem = Pesagem.objects.create(
            data=dto.data,
            prefixo_id_id=dto.prefixo_id,  # Django ORM espera <field>_id para FK
            cooperativa_id_id=dto.cooperativa_id,
            responsavel_coop=dto.responsavel_coop,
            motorista_id_id=dto.motorista_id,
            hora_chegada=dto.hora_chegada,
            hora_saida=dto.hora_saida,
            numero_doc=dto.numero_doc,
            volume_carga=dto.volume_carga,
            tipo_pesagem=dto.tipo_pesagem,
            garagem=dto.garagem,
            turno=dto.turno
        )

        # Vincula colaboradores (ManyToMany)
        if dto.colaborador_ids:
            colaboradores = Colaborador.objects.filter(id__in=dto.colaborador_ids)
            pesagem.colaborador_id.set(colaboradores)

        return pesagem.id

    
#### pesagem listar mapper
class PesagemListMapper:
    @staticmethod
    def listar(dto):
        where = []
        params = []

        if dto.start_date:
            where.append("p.data >= %s")
            params.append(dto.start_date)

        if dto.end_date:
            where.append("p.data <= %s")
            params.append(dto.end_date)

        if dto.tipo_pesagem:
            where.append("p.tipo_pesagem = %s")
            params.append(dto.tipo_pesagem)

        if dto.cursor is not None:
            where.append("p.id < %s")
            params.append(dto.cursor)

        where_sql = " AND ".join(where)
        where_sql = f"AND {where_sql}" if where_sql else ""

        sql = f"""
            SELECT
                p.id, p.data, p.tipo_pesagem, p.peso_calculado
            FROM pesagem p
            WHERE 1=1
            {where_sql}
            ORDER BY {order_sql_pesagem(dto.ordering)}
            LIMIT %s
        """

        params.append(dto.limit + 1)

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        columns = ("id", "data", "tipo_pesagem", "peso_calculado")
        return [dict(zip(columns, r)) for r in rows]

    @staticmethod
    def totais(dto):
        where = []
        params = []

        if dto.start_date:
            where.append("data >= %s")
            params.append(dto.start_date)

        if dto.end_date:
            where.append("data <= %s")
            params.append(dto.end_date)

        where_sql = " AND ".join(where)
        where_sql = f"WHERE {where_sql}" if where_sql else ""

        sql = f"""
            SELECT
                COUNT(*) as total_pesagens,
                COALESCE(SUM(peso_calculado), 0) as total_peso
            FROM pesagem
            {where_sql}
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            row = cursor.fetchone()

        return {
            "total_pesagens_all": row[0],
            "total_peso_all": float(row[1]),
        }

### retorna quantidade catatreco e seletiva
class PesagemTipoServicoMapper:
    @staticmethod
    def total(tipo_pesagem: str) -> int:
        with connection.cursor() as c:
            c.execute(
                "SELECT COUNT(*) FROM pesagem WHERE tipo_pesagem = %s",
                [tipo_pesagem],
            )
            return c.fetchone()[0]



class PesagemFiltersMapper:
    @staticmethod
    def filter(filters: dict):
        sql = """
        SELECT p.*
        FROM pesagem p
        LEFT JOIN prefixo pf ON pf.id = p.prefixo_id
        LEFT JOIN cooperativa c ON c.id = p.cooperativa_id
        WHERE 1=1
        """
        params = []
        mapping = {
            "start_date": ("p.data >= %s", lambda v: v),
            "end_date": ("p.data <= %s", lambda v: v),
            "prefixo": ("pf.prefixo LIKE %s", lambda v: f"{v}%"),
            "tipo_pesagem": ("p.tipo_pesagem = %s", lambda v: v),
            "volume_carga": ("p.volume_carga = %s", lambda v: v),
            "cooperativa": ("c.nome = %s", lambda v: v),
            "responsavel_coop": ("p.responsavel_coop LIKE %s", lambda v: f"%{v}%"),
            "garagem": ("p.garagem = %s", lambda v: v),
            "turno": ("p.turno = %s", lambda v: v),
        }

        # Aplica filtros simples
        for key, (clause, func) in mapping.items():
            if filters.get(key):
                sql += f" AND {clause}"
                params.append(func(filters[key]))

        # Filtro especial para numero_doc (simula regex simples)
        if filters.get("numero_doc"):
            val = filters["numero_doc"]
            # numero_doc começa com valor, opcionalmente seguido de letra
            sql += " AND (p.numero_doc = %s OR p.numero_doc LIKE %s)"
            params.extend([val, f"{val}_"])

        with connection.cursor() as c:
            c.execute(sql, params)
            # Converte cada linha em dict
            columns = [col[0] for col in c.description]
            return [dict(zip(columns, row)) for row in c.fetchall()]