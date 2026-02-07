import datetime
from django.db.models import Q, Count
from apps.averiguacao.models.averiguacao import Averiguacao
from apps.averiguacao.dto.averiguacao_dto import AveriguacaoCreateRequestDTO,AveriguacaoResponseDTO
from apps.averiguacao.utils.averiguacao_utils import (
    PA_ESTABELECIDAS,
    METAS_SEMANAIS,
    calcular_periodo_semana,
)


class AveriguacaoCreateMapper:
    @staticmethod
    def insert(dto: AveriguacaoCreateRequestDTO) -> int:
        averiguacao = Averiguacao.objects.create(
            tipo_servico=dto.tipo_servico,
            pa_da_averiguacao=dto.pa_da_averiguacao,
            rota_averiguada_id=dto.rota_averiguada_id,
            averiguador=dto.averiguador,
            formulario=dto.formulario,
        )
        return averiguacao.id
    

class AveriguacaoResponseMapper:
    @staticmethod
    def from_model(obj: Averiguacao) -> AveriguacaoResponseDTO:
        return AveriguacaoResponseDTO(
            id=obj.id,
            tipo_servico=obj.tipo_servico,
            pa_da_averiguacao=obj.pa_da_averiguacao,
            data=obj.data,
            hora_averiguacao=obj.hora_averiguacao,
            rota_averiguada_id=obj.rota_averiguada_id,

            imagem1=obj.imagem1.url if obj.imagem1 else None,
            imagem2=obj.imagem2.url if obj.imagem2 else None,
            imagem3=obj.imagem3.url if obj.imagem3 else None,
            imagem4=obj.imagem4.url if obj.imagem4 else None,
            imagem5=obj.imagem5.url if obj.imagem5 else None,
            imagem6=obj.imagem6.url if obj.imagem6 else None,
            imagem7=obj.imagem7.url if obj.imagem7 else None,

            averiguador=obj.averiguador,
            formulario=obj.formulario,
        )

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
