import datetime
from django.db.models import Q, Count
from apps.averiguacao.models.averiguacao import Averiguacao
from apps.averiguacao.dto.averiguacao_dto import AveriguacaoCreateDTO
from apps.averiguacao.utils.averiguacao_utils import (
    PA_ESTABELECIDAS,
    METAS_SEMANAIS,
    calcular_periodo_semana,
)


class AveriguacaoCreateMapper:
    @staticmethod
    def insert(dto: AveriguacaoCreateDTO) -> int:
        averiguacao = Averiguacao.objects.create(
            tipo_servico=dto.tipo_servico,
            pa_da_averiguacao=dto.pa_da_averiguacao,
            data=dto.data,
            hora_averiguacao=dto.hora_da_averiguacao,
            rota_da_averiguacao=dto.rota_da_averiguacao,
            imagem1=dto.imagem1,
            imagem2=dto.imagem2,
            imagem3=dto.imagem3,
            imagem4=dto.imagem4,
            imagem5=dto.imagem5,
            imagem6=dto.imagem6,
            imagem7=dto.imagem7,
        )
        return averiguacao.id

class AveriguacaoEstatisticasSemanaMapper:
    @classmethod
    def map_cards_semana(cls, pa, turno, servico, data_inicio=None, data_fim=None):
        inicio, fim = calcular_periodo_semana(data_inicio, data_fim)

        filtro = Q(
            tipo_servico=servico,
            data__range=(inicio, fim),
        )

        if pa:
            filtro &= Q(pa_da_averiguacao=pa)

        if turno:
            filtro &= Q(rota_averiguada__turno=turno)

        queryset = (
            Averiguacao.objects
            .filter(filtro)
            .values("data", "pa_da_averiguacao")
            .annotate(total=Count("id"))
        )

        dias = [
            (inicio + datetime.timedelta(days=i)).isoformat()
            for i in range(7)
        ]

        cards_por_dia = {
            dia: {pa: 0 for pa in PA_ESTABELECIDAS}
            for dia in dias
        }

        for row in queryset:
            dia = row["data"].isoformat()
            cards_por_dia[dia][row["pa_da_averiguacao"]] = row["total"]

        return cards_por_dia, inicio, fim

    @classmethod
    def map_meta(cls, servico, cards_por_dia):
        meta_total = METAS_SEMANAIS.get(servico, 0)

        total_realizado = sum(
            qtd for dia in cards_por_dia.values()
            for qtd in dia.values()
        )

        total_faltante = max(meta_total - total_realizado, 0)

        return {
            "total": meta_total,
            "realizado": total_realizado,
            "percentual_realizado": round(
                (total_realizado / meta_total) * 100, 2
            ) if meta_total else 0,
            "faltante": total_faltante,
            "percentual_faltante": round(
                (total_faltante / meta_total) * 100, 2
            ) if meta_total else 0,
        }
