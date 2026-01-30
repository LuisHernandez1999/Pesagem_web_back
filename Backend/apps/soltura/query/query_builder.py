from apps.soltura.utils.filters_utils import SolturaFilterBuilder
from apps.soltura.mappers.soltura_mapper import SolturaQuerySetMapper
####### builder de query
class SolturaListQueryBuilder:
    @staticmethod
    def build(config, filtro, cursor):
        qs = config.queryset()
        qs = SolturaFilterBuilder.apply_base(qs, config.filtro_fn, filtro)
        qs = SolturaFilterBuilder.apply_global_search(qs, filtro.search)
        qs = SolturaFilterBuilder.apply_column_filters(qs, filtro.column_filters)
        qs = SolturaQuerySetMapper.aplicar_cursor(qs, cursor)
        return SolturaQuerySetMapper.ordenar(qs)