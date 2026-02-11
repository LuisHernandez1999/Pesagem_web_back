from dataclasses import asdict
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db import transaction
from datetime import date
from apps.soltura.dto.soltura_dtos  import ListResponseDTO,SolturaAnalyticsFiltroDTO
from apps.soltura.query.pagination import CursorPaginator
from apps.soltura.query.config import SOLTURA_RESUMO_CONFIG
from apps.soltura.mappers.soltura_mapper import (SolturaAnalyticsQuerySetMapper,SolturaAnalyticsResultMapper,SolturaQuerySetMapper)
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


class SolturaResumoService:
    @classmethod
    def executar(cls, termo=None, cursor=None, tipo_servico=None):
        """
        Retorna o resumo das solturas.
        - Se tipo_servico for passado, retorna apenas aquele serviço (limit 10).
        - Caso contrário, retorna todos os serviços de acordo com SOLTURA_RESUMO_CONFIG.
        """
        items = {}
        cursores = {}

        if tipo_servico:
            # Filtra apenas o serviço solicitado
            cfg = next((c for c in SOLTURA_RESUMO_CONFIG if c[0] == tipo_servico.lower()), None)
            if not cfg:
                raise ValidationError("tipo_servico inválido")

            key, base_qs_fn, mapper, _ = cfg

            qs = base_qs_fn()
            qs = SolturaQuerySetMapper.aplicar_busca_global(qs, termo)
            qs = SolturaQuerySetMapper.ordenar(qs)
            total = qs.count()
            qs = SolturaQuerySetMapper.aplicar_cursor(qs, cursor)
            rows, next_cursor = CursorPaginator.paginar(qs, 10)  # Sempre 10 por página

            items[key] = [mapper.from_model(o) for o in rows]
            cursores[key] = next_cursor

        else:
            # Sem filtro, percorre todos os tipos
            for key, base_qs_fn, mapper, limit in SOLTURA_RESUMO_CONFIG:
                qs = base_qs_fn()
                qs = SolturaQuerySetMapper.aplicar_busca_global(qs, termo)
                qs = SolturaQuerySetMapper.ordenar(qs)
                total = qs.count()
                qs = SolturaQuerySetMapper.aplicar_cursor(qs, cursor)
                rows, next_cursor = CursorPaginator.paginar(qs, limit)

                items[key] = [mapper.from_model(o) for o in rows]
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