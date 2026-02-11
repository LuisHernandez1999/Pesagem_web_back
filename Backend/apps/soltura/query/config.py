from apps.soltura.mappers.soltura_mapper import (
     SolturaQuerySetMapper,
    SeletivaListMapper,
    RemocaoListMapper,
    DomiciliarListMapper,
)


SOLTURA_RESUMO_CONFIG = (
    ("seletiva", lambda: SolturaQuerySetMapper.base("Seletiva"), SeletivaListMapper, 4),
    ("remocao", lambda: SolturaQuerySetMapper.base("Remoção"), RemocaoListMapper, 3),
    ("domiciliar", lambda: SolturaQuerySetMapper.base("Domiciliar"), DomiciliarListMapper, 3),
)
