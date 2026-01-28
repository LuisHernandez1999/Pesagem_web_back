from django.db.models import Count
from django.db import transaction
from apps.soltura.models.soltura import Soltura
from apps.colaborador.models.colaborador import Colaborador
from apps.soltura.dto.remocao_dto import SolturaFiltroDTO,SolturaCreateDTO,SolturaCreateResponseDTO
from apps.soltura.mappers.remocao_mappers import SolturaRemocaoMapper,SolturaCreateMapper
from apps.soltura.utils.cache_utils import memoize_with_ttl
from apps.soltura.utils.filters_utils import montar_filtro_domiciliar
from apps.soltura.dto.remocao_dto import SolturaListOutputDTO
from apps.soltura.mappers.remocao_mappers import RemocaoQuerySetMapper
from apps.soltura.mappers.remocao_mappers import RemocaoListMapper
from apps.soltura.utils.remocao_validacao_utils import validar_coletores,validar_motorista,validar_veiculo



class ServiceDomiciliarList:
    @staticmethod
    @memoize_with_ttl(ttl_seconds=300)
    def executar(dto: SolturaFiltroDTO):
        filtros = montar_filtro_domiciliar(dto)
        qs = (
            Soltura.objects
            .filter(filtros)
            .values("status", "data_soltura")
            .annotate(total=Count("id"))
        )
        return SolturaRemocaoMapper.from_queryset(qs)
    
