from django.db.models import Q
from datetime import date
from apps.soltura.dto.remocao_dto import SolturaFiltroDTO


def montar_filtro_remocao(dto: SolturaFiltroDTO) -> Q:
    today = date.today()
    start_date = dto.start_date or date(today.year, 1, 1)
    end_date = dto.end_date or today

    filtros = (
        Q(tipo_servico__iexact="Remoção") &
        Q(data_soltura__range=[start_date, end_date])
    )

    if dto.status:
        filtros &= Q(status__iexact=dto.status)

    return filtros



def montar_filtro_domiciliar(dto: SolturaFiltroDTO) -> Q:
    today = date.today()
    start_date = dto.start_date or date(today.year, 1, 1)
    end_date = dto.end_date or today

    filtros = (
        Q(tipo_servico__iexact="Domiciliar") &
        Q(data_soltura__range=[start_date, end_date])
    )

    if dto.status:
        filtros &= Q(status__iexact=dto.status)

    return filtros