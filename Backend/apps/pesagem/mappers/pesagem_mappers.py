from django.db import connection
from apps.pesagem.models import Pesagem, Colaborador 


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
    def list(dto):
        sql = """
        SELECT
            p.id,
            p.data,
            p.tipo_pesagem,
            p.volume_carga,
            p.numero_doc,
            p.peso_calculado,
            p.responsavel_coop,
            p.garagem,
            p.turno,
            v.prefixo AS prefixo,
            m.nome AS motorista,
            c.nome AS cooperativa
        FROM pesagem p
        INNER JOIN veiculo v ON v.id = p.prefixo_id
        INNER JOIN colaborador m ON m.id = p.motorista_id
        INNER JOIN cooperativa c ON c.id = p.cooperativa_id
        WHERE 1=1
        """

        params = []

        if dto.start_date:
            sql += " AND p.data >= %s"
            params.append(dto.start_date)

        if dto.end_date:
            sql += " AND p.data <= %s"
            params.append(dto.end_date)

        if dto.prefixo:
            sql += " AND v.prefixo LIKE %s"
            params.append(f"{dto.prefixo}%")

        if dto.motorista:
            sql += " AND m.nome LIKE %s"
            params.append(f"%{dto.motorista}%")

        if dto.tipo_pesagem:
            sql += " AND p.tipo_pesagem = %s"
            params.append(dto.tipo_pesagem)

        if dto.volume_carga:
            sql += " AND p.volume_carga = %s"
            params.append(dto.volume_carga)

        if dto.cooperativa:
            sql += " AND c.nome = %s"
            params.append(dto.cooperativa)

        if dto.numero_doc:
            sql += " AND p.numero_doc LIKE %s"
            params.append(f"{dto.numero_doc}%")

        if dto.responsavel_coop:
            sql += " AND p.responsavel_coop LIKE %s"
            params.append(f"%{dto.responsavel_coop}%")

        if dto.garagem:
            sql += " AND p.garagem = %s"
            params.append(dto.garagem)

        if dto.turno:
            sql += " AND p.turno = %s"
            params.append(dto.turno)

        # cursor pagination
        if dto.cursor_id:
            sql += " AND p.id < %s"
            params.append(dto.cursor_id)

        sql += " ORDER BY p.id DESC LIMIT %s"
        params.append(dto.limit + 1)

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            columns = [c[0] for c in cursor.description]

        results = [dict(zip(columns, r)) for r in rows]

        next_cursor = None
        if len(results) > dto.limit:
            next_cursor = results[-1]["id"]
            results = results[:-1]

        return results, next_cursor



class ExibirPesagemPorMesMapper:
    @staticmethod
    def fetch(dto):
        sql = """
        SELECT
            strftime('%Y', p.data) AS ano,
            strftime('%m', p.data) AS mes_referencia,
            p.tipo_pesagem,
            COUNT(p.id) AS quantidade_pesagens,
            ROUND(SUM(COALESCE(p.peso_calculado, 0)), 2) AS peso_total
        FROM pesagem p
        WHERE
            p.data IS NOT NULL
            AND p.tipo_pesagem IS NOT NULL
        """

        params = []

        if dto.start_date:
            sql += " AND p.data >= %s"
            params.append(dto.start_date)

        if dto.end_date:
            sql += " AND p.data <= %s"
            params.append(dto.end_date)

        if dto.tipo_pesagem:
            sql += " AND p.tipo_pesagem = %s"
            params.append(dto.tipo_pesagem)

        sql += """
        GROUP BY
            ano,
            mes_referencia,
            p.tipo_pesagem
        ORDER BY
            ano DESC,
            mes_referencia DESC
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

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