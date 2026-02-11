from django.core.exceptions import ValidationError
from django.db.models import Q
from apps.soltura.models.soltura import Soltura
from django.db import transaction
from apps.soltura.dto.soltura_dtos  import ListResponseDTO,SolturaAnalyticsFiltroDTO
from apps.soltura.query.config import SOLTURA_RESUMO_CONFIG
from apps.soltura.mappers.soltura_mapper import (SolturaAnalyticsQuerySetMapper,SolturaAnalyticsResultMapper,
                                                 SolturaQuerySetMapper,SolturaMapperUpdate,SolturaMapperCreate)
from apps.soltura.utils.cache_utils import memoize_with_ttl
from apps.soltura.dto.soltura_dtos import SolturaCreateDTO
from apps.soltura.utils.soltura_create_utils import validar_soltura
from apps.soltura.utils.filters_utils import processar_qs


class SolturaServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: SolturaCreateDTO) -> int:
        validar_soltura(dto)
        soltura_id = SolturaMapperCreate.insert(dto)
        return soltura_id


class SolturaEditService:
    @staticmethod
    def edit_soltura(soltura_id, dto):
        try:
            return SolturaMapperUpdate.update(soltura_id, dto)
        except Soltura.DoesNotExist:
            raise ValueError(f"Soltura com id {soltura_id} não encontrada")


class SolturaResumoService:
    @classmethod
    def executar(cls, termo=None, cursor=None, tipo_servico=None):
        items = {}
        cursores = {}
        total = 0
        configs = (
            [c for c in SOLTURA_RESUMO_CONFIG if c[0] == tipo_servico.lower()]
            if tipo_servico else SOLTURA_RESUMO_CONFIG
        )
        if tipo_servico and not configs:
            raise ValidationError("tipo_servico inválido")

        for key, base_qs_fn, mapper, limit in configs:
            qs = base_qs_fn()
            itens, next_cursor, total = processar_qs(qs, termo, cursor, limit, mapper)
            items[key] = itens
            cursores[key] = next_cursor
        return ListResponseDTO(
            items=items,
            total=total,
            next_cursor=cursores
        )


class SolturaAnalyticsService:
    @staticmethod
    @memoize_with_ttl(ttl_seconds=300)
    def executar(dto: SolturaAnalyticsFiltroDTO):
        filtros = Q()  
        filtros &= dto.filtro_fn(dto)
        if dto.status:
            filtros &= Q(status__iexact=dto.status)
        if dto.data_inicio and dto.data_fim:
            filtros &= Q(data_soltura__range=[dto.data_inicio, dto.data_fim])
        qs = SolturaAnalyticsQuerySetMapper.build(filtros)
        return SolturaAnalyticsResultMapper.map(qs)