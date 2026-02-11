from collections import defaultdict
from django.db.models import Q, Count
from apps.soltura.models import Soltura
from apps.soltura.dto.soltura_dtos import SolturaListItemDTO


class SolturaMapperCreate:
    @staticmethod
    def insert(dto) -> int:
        soltura = Soltura.objects.create(
            tipo_servico=dto.tipo_servico,
            garagem=dto.garagem,
            turno=dto.turno,
            hora_entrega_chave=dto.hora_entrega_chave,
            hora_saida_frota=dto.hora_saida_frota,
            data_soltura=dto.data_soltura,
            status=dto.status,
            veiculo_id=dto.veiculo_id,
            rota_id=dto.rota_id,
            motorista_id=dto.motorista_id,
        )

        if dto.coletores_ids:
            Soltura.coletores.through.objects.bulk_create(
                [
                    Soltura.coletores.through(
                        soltura_id=soltura.id,
                        coletores_id=cid
                    )
                    for cid in dto.coletores_ids
                ],
                batch_size=100
            )

        return soltura.id
    
class BaseSolturaListMapper:
    rota_field = False
    setor_field = False

    @classmethod
    def from_model(cls, s):
        return SolturaListItemDTO(
            id=s.id,

            motorista=s.motorista.nome,

            # ✅ MANY TO MANY — lista de nomes
            coletores=[c.nome for c in s.coletores.all()],

            garagem=s.garagem,
            data_soltura=s.data_soltura,

            rota=s.rota.rota if cls.rota_field and s.rota_id else None,
            setor=s.setor.nome_setor if cls.setor_field and s.setor_id else None,

            turno=s.turno,
            status=s.status,
            prefixo=s.veiculo.prefixo,
        )

class RemocaoListMapper(BaseSolturaListMapper):
    setor_field = True


class SeletivaListMapper(BaseSolturaListMapper):
    rota_field = True


class DomiciliarListMapper(SeletivaListMapper):
    pass

class SolturaQuerySetMapper:
    @staticmethod
    def base(tipo_servico):
        return (
            Soltura.objects
            .filter(tipo_servico=tipo_servico)
            .select_related("motorista", "rota", "setor", "veiculo")
            .prefetch_related("coletores")
            .only(
                "id",
                "data_soltura",
                "garagem",
                "turno",
                "status",
                "motorista__nome",
                "veiculo__prefixo",
                "rota__rota",
                "setor__nome_setor",
            )
        )

    @staticmethod
    def aplicar_cursor(qs, cursor):
        if not cursor:
            return qs
        return qs.filter(
            Q(data_soltura__lt=cursor.data_soltura)
            | Q(data_soltura=cursor.data_soltura, id__lt=cursor.id)
        )

    @staticmethod
    def aplicar_busca_global(qs, termo):
        if not termo:
            return qs
        q = Q()
        for palavra in termo.split():
            q |= Q(motorista__nome__icontains=palavra)
            q |= Q(veiculo__prefixo__icontains=palavra)
        return qs.filter(q)

    @staticmethod
    def ordenar(qs):
        return qs.order_by("-data_soltura", "-id")
    
class SolturaAnalyticsQuerySetMapper:
    @staticmethod
    def build(filtros):
        return (
            Soltura.objects
            .filter(filtros)
            .values("status", "data_soltura")
            .annotate(total=Count("id"))
        )


class SolturaAnalyticsResultMapper:
    @staticmethod
    def map(qs):
        em_andamento = 0
        concluido = 0

        por_dia = defaultdict(int)
        por_mes = defaultdict(int)
        por_dia_semana = defaultdict(int)

        for r in qs:
            total = r["total"]
            data = r["data_soltura"]
            status = (r["status"] or "").lower()

            if status == "em andamento":
                em_andamento += total
            elif status == "concluído":
                concluido += total

            if data:
                por_dia[data.isoformat()] += total
                por_mes[data.month] += total
                por_dia_semana[data.isoweekday()] += total

        return {
            "total_em_andamento": em_andamento,
            "total_concluido": concluido,
            "contagem_dia": dict(por_dia),
            "contagem_mes": dict(por_mes),
            "contagem_dia_semana": dict(por_dia_semana),
            "mes_mais_saida": max(por_mes, key=por_mes.get) if por_mes else None,
        }
