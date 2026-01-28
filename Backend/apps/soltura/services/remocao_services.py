from django.db.models import Count
from django.db import transaction
from apps.soltura.models.soltura import Soltura
from apps.colaborador.models.colaborador import Colaborador
from apps.soltura.dto.remocao_dto import SolturaFiltroDTO,SolturaCreateDTO,SolturaCreateResponseDTO
from apps.soltura.mappers.remocao_mappers import SolturaRemocaoMapper,SolturaCreateMapper
from apps.soltura.utils.cache_utils import memoize_with_ttl
from apps.soltura.utils.filters_utils import montar_filtro_remocao
from apps.soltura.dto.remocao_dto import SolturaListOutputDTO
from apps.soltura.mappers.remocao_mappers import RemocaoQuerySetMapper
from apps.soltura.mappers.remocao_mappers import RemocaoListMapper
from apps.soltura.utils.remocao_validacao_utils import validar_coletores,validar_motorista,validar_veiculo


class SolturaRemocaoStatsService:
    @staticmethod
    @memoize_with_ttl(ttl_seconds=300)
    def executar(dto: SolturaFiltroDTO):
        filtros = montar_filtro_remocao(dto)
        qs = (
            Soltura.objects
            .filter(filtros)
            .values("status", "data_soltura")
            .annotate(total=Count("id"))
        )
        return SolturaRemocaoMapper.from_queryset(qs)
    


class RemocaoListService:
    @staticmethod
    def executar(dto):
        qs = RemocaoQuerySetMapper.base_queryset()
        qs = RemocaoQuerySetMapper.aplicar_cursor(qs, dto.cursor)
        qs = RemocaoQuerySetMapper.aplicar_filtros(qs, dto.filters)
        qs = RemocaoQuerySetMapper.aplicar_date_range(qs, dto.start_date, dto.end_date)
        qs = RemocaoQuerySetMapper.aplicar_search(qs, dto.search)
        qs = RemocaoQuerySetMapper.aplicar_busca_global(qs, dto.q)
        qs = RemocaoQuerySetMapper.ordenar(qs)
        qs = RemocaoQuerySetMapper.paginar(qs, dto.page_size)
        items = [RemocaoListMapper.from_model(s) for s in qs]
        next_cursor = None
        if items:
            last = items[-1]
            next_cursor = {
                "data_soltura": last.data_soltura,
                "id": last.id
            }
        return SolturaListOutputDTO(
            items=items,
            next_cursor=next_cursor
        )




class SolturaCreateService:
    @staticmethod
    @transaction.atomic
    def executar(dto: SolturaCreateDTO) -> SolturaCreateResponseDTO:
        motorista = Colaborador.objects.get(id=dto.motorista_id)

        validar_motorista(motorista)

        soltura = SolturaCreateMapper.from_dto(dto)

        validar_veiculo(soltura.veiculo)

        soltura.full_clean()
        soltura.save()

        if dto.coletores_ids:
            soltura.coletores.set(dto.coletores_ids)

        validar_coletores(
            list(soltura.coletores.all()),
            dto.tipo_servico
        )

        return SolturaCreateResponseDTO(
            id=soltura.id,
            status=soltura.status,
            tipo_servico=soltura.tipo_servico,
            data_soltura=soltura.data_soltura
        )

