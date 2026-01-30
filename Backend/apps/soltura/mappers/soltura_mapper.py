from apps.soltura.dto.soltura_dtos import SolturaListItemDTO
from django.db.models import Q,Count,F, Func
from django.db.models.functions import ExtractMonth, ExtractWeekDay
from apps.soltura.models import Soltura
from apps.colaborador.models.colaborador import Colaborador
from apps.veiculo.models.veiculo import Veiculo
from apps.soltura.models.rota import Rota
from collections import defaultdict


########mapper de create
class SolturaMapperCreate:
    @staticmethod
    def insert(dto) -> int:
        veiculo = Veiculo.objects.get(id=dto.veiculo_id)

        rota = Rota.objects.get(
            id=dto.rota_id
        )

        motorista = Colaborador.objects.get(id=dto.motorista_id)
        coletores = Colaborador.objects.filter(id__in=dto.coletores_ids)

        soltura = Soltura.objects.create(
            tipo_servico=dto.tipo_servico,
            garagem=dto.garagem,
            turno=dto.turno,
            hora_entrega_chave=dto.hora_entrega_chave,
            hora_saida_frota=dto.hora_saida_frota,
            rota=rota,
            data_soltura=dto.data_soltura,
            veiculo=veiculo,
            motorista=motorista,
            status=dto.status,
        )

        if coletores.exists():
            soltura.coletores.set(coletores)

        return soltura.id


########### query de remocao
class RemocaoListMapper:
    @staticmethod
    def from_model(s):
        return SolturaListItemDTO(
            id=s.id,
            motorista=s.motorista.nome if s.motorista else None,
            coletores=[c.nome for c in s.coletores.all()],
            garagem=s.garagem,
            data_soltura=s.data_soltura,
            rota=None,
            setor=s.setor.nome_setor if s.setor else None,
            turno=s.turno,
            status=s.status,
            prefixo=s.veiculo.prefixo if s.veiculo else None,
        )

class SeletivaListMapper:
    @staticmethod
    def from_model(s):
        return SolturaListItemDTO(
            id=s.id,
            motorista=s.motorista.nome if s.motorista else None,
            coletores=[c.nome for c in s.coletores.all()],
            garagem=s.garagem,
            data_soltura=s.data_soltura,
            rota=s.rota.rota if s.rota else None,
            setor=None,
            turno=s.turno,
            status=s.status,
            prefixo=s.veiculo.prefixo if s.veiculo else None,
        )

class DomiciliarListMapper(SeletivaListMapper):
    pass

######## querysets base
class SolturaQuerySetMapper:
    @staticmethod
    def base_remocao():
        return (
            Soltura.objects
            .filter(tipo_servico="Remoção")
            .select_related("motorista", "setor", "veiculo")
            .prefetch_related("coletores")
            .only(
                "id", "data_soltura", "garagem", "turno", "status",
                "motorista__nome", "setor__nome_setor", "veiculo__prefixo"
            )
        )
    @staticmethod
    def base_seletiva():
        return (
            Soltura.objects
            .filter(tipo_servico="Seletiva")
            .select_related("motorista", "rota", "veiculo")
            .prefetch_related("coletores")
            .only(
                "id", "data_soltura", "garagem", "turno", "status",
                "motorista__nome", "rota__rota", "veiculo__prefixo"
            )
        )

    @staticmethod
    def base_domiciliar():
        return (
            Soltura.objects
            .filter(tipo_servico="Domiciliar")
            .select_related("motorista", "rota", "veiculo")
            .prefetch_related("coletores")
            .only(
                "id", "data_soltura", "garagem", "turno", "status",
                "motorista__nome", "rota__rota", "veiculo__prefixo"
            )
        )

    @staticmethod
    def aplicar_cursor(qs, cursor):
        if not cursor:
            return qs
        return qs.filter(
            Q(data_soltura__lt=cursor.data_soltura) |
            Q(data_soltura=cursor.data_soltura, id__lt=cursor.id)
        )

    @staticmethod
    def aplicar_busca_global(qs, termo):
        if not termo:
            return qs
        q = Q()
        for p in termo.split():
            q |= (
                Q(motorista__nome__icontains=p) |
                Q(veiculo__prefixo__icontains=p)
            )
        return qs.filter(q)

    @staticmethod
    def ordenar(qs):
        return qs.order_by("-data_soltura", "-id")

###### mappers de graficos
class SolturaAnalyticsQuerySetMapper:
    @staticmethod
    def build(filtros):
        return (
            Soltura.objects
            .filter(filtros)
            .values("status", "data_soltura")
            .annotate(total=Count("id"))
        )
###### mappers de graficos RESULTADOS 
class SolturaAnalyticsResultMapper:
    @staticmethod
    def map(qs):
        total_em_andamento = 0
        total_concluido = 0

        por_dia = defaultdict(int)
        por_mes = defaultdict(int)
        por_dia_semana = defaultdict(int)

        for row in qs:
            status = (row.get("status") or "").lower()
            total = row.get("total", 0)
            data = row.get("data_soltura")

            if status == "em andamento":
                total_em_andamento += total
            elif status == "concluído":
                total_concluido += total

            if data:
                por_dia[data.strftime("%Y-%m-%d")] += total
                por_mes[data.month] += total
                por_dia_semana[data.isoweekday()] += total

        return {
            "total_em_andamento": total_em_andamento,
            "total_concluido": total_concluido,
            "contagem_dia": dict(por_dia),
            "contagem_mes": dict(por_mes),
            "contagem_dia_semana": dict(por_dia_semana),
            "mes_mais_saida": max(por_mes, key=por_mes.get) if por_mes else None,
        }