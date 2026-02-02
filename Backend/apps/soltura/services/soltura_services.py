from dataclasses import asdict
from django.db.models import Q
from django.db import transaction
from datetime import date
from apps.soltura.dto.soltura_dtos  import ListResponseDTO,SolturaAnalyticsFiltroDTO
from apps.soltura.query.query_builder import SolturaListQueryBuilder
from apps.soltura.query.pagination import CursorPaginator
from apps.soltura.query.config import SOLTURA_CONFIG
from apps.soltura.mappers.soltura_mapper import SolturaAnalyticsQuerySetMapper,SolturaAnalyticsResultMapper
from apps.soltura.utils.cache_utils import memoize_with_ttl
from apps.soltura.dto.soltura_dtos import SolturaCreateDTO
from apps.soltura.utils.soltura_create_utils import validar_soltura
from apps.soltura.mappers.soltura_mapper import SolturaMapperCreate


class SolturaServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: SolturaCreateDTO) -> int:
        validar_soltura(dto)
        soltura_id = SolturaMapperCreate.insert(dto)
        return soltura_id


class SolturaListService:
    @staticmethod
    @memoize_with_ttl(ttl_seconds=300)
    def listar(dto):
        config = SOLTURA_CONFIG[dto.tipo_servico]
        qs = SolturaListQueryBuilder.build(
            config, dto.filtro, dto.cursor
        )
        total = qs.count()
        rows, next_cursor = CursorPaginator.paginar(
            qs, dto.filtro.limit
        )
        return ListResponseDTO(
            items=[config.mapper.from_model(r) for r in rows],
            total=total,
            next_cursor=asdict(next_cursor) if next_cursor else None
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