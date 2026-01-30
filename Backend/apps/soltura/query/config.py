from apps.soltura.mappers.soltura_mapper import SolturaQuerySetMapper
from apps.soltura.mappers.soltura_mapper import (
    RemocaoListMapper, SeletivaListMapper, DomiciliarListMapper
)
from apps.soltura.utils.filters_utils import (
    filtro_remocao, filtro_seletiva, filtro_domiciliar
)

class SolturaListConfig:
    def __init__(self, queryset, filtro_fn, mapper):
        self.queryset = queryset
        self.filtro_fn = filtro_fn
        self.mapper = mapper

SOLTURA_CONFIG = {
    "Remoção": SolturaListConfig(
        SolturaQuerySetMapper.base_remocao,
        filtro_remocao,
        RemocaoListMapper,
    ),
    "Seletiva": SolturaListConfig(
        SolturaQuerySetMapper.base_seletiva,
        filtro_seletiva,
        SeletivaListMapper,
    ),
    "Domiciliar": SolturaListConfig(
        SolturaQuerySetMapper.base_domiciliar,
        filtro_domiciliar,
        DomiciliarListMapper,
    ),
}
