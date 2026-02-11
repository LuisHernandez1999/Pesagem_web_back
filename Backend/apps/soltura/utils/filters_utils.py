from django.db.models import Q
from django.core.exceptions import ValidationError

from apps.soltura.query.config import SOLTURA_RESUMO_CONFIG
from apps.soltura.mappers.soltura_mapper import SolturaQuerySetMapper
from apps.soltura.dto.soltura_dtos import ListResponseDTO
from apps.soltura.query.pagination import CursorPaginator


def processar_qs(qs, termo=None, cursor=None, limit=10, mapper=None):
    qs = SolturaQuerySetMapper.aplicar_busca_global(qs, termo)
    qs = SolturaQuerySetMapper.ordenar(qs)
    total = qs.count()
    qs = SolturaQuerySetMapper.aplicar_cursor(qs, cursor)
    rows, next_cursor = CursorPaginator.paginar(qs, limit)
    items = [mapper.from_model(o) for o in rows] if mapper else []
    return items, next_cursor, total



def listar_por_tipo(tipo_servico, termo, cursor):
    cfg = (SOLTURA_RESUMO_CONFIG, tipo_servico.lower())
    if not cfg:
        raise ValidationError("tipo_servico inválido")
    key, base_qs_fn, mapper, _ = cfg

    qs = base_qs_fn()
    qs = SolturaQuerySetMapper.aplicar_busca_global(qs, termo)
    qs = SolturaQuerySetMapper.ordenar(qs)

    total = qs.count()

    qs = SolturaQuerySetMapper.aplicar_cursor(qs, cursor)
    rows, next_cursor = CursorPaginator.paginar(qs, 10)

    return ListResponseDTO(
        items={key: [mapper.from_model(o) for o in rows]},
        total=total,
        next_cursor={key: next_cursor}
    )


def listar_resumo(termo, cursor):
    items = {}
    cursores = {}

    for key, base_qs_fn, mapper, limit in SOLTURA_RESUMO_CONFIG:
        qs = base_qs_fn()
        qs = SolturaQuerySetMapper.aplicar_busca_global(qs, termo)
        qs = SolturaQuerySetMapper.ordenar(qs)
        qs = SolturaQuerySetMapper.aplicar_cursor(qs, cursor)

        rows, next_cursor = CursorPaginator.paginar(qs, limit)

        items[key] = [mapper.from_model(o) for o in rows]
        cursores[key] = next_cursor

    total = sum(limit for *_, limit in SOLTURA_RESUMO_CONFIG)

    return ListResponseDTO(
        items=items,
        total=total,
        next_cursor=cursores
    )


COLUMN_MAP = {
    "motorista": "motorista__nome",
    "prefixo": "veiculo__prefixo",
    "rota": "rota__rota",
    "status": "status",
    "garagem": "garagem",
}

class SolturaFilterBuilder:

    @staticmethod
    def apply_base(qs, filtro_fn, dto):
        qs = qs.filter(filtro_fn(dto))

        if dto.status:
            qs = qs.filter(status__iexact=dto.status)

        if dto.data_inicio and dto.data_fim:
            qs = qs.filter(
                data_soltura__range=[dto.data_inicio, dto.data_fim]
            )
        elif dto.data_inicio:
            qs = qs.filter(data_soltura__gte=dto.data_inicio)
        elif dto.data_fim:
            qs = qs.filter(data_soltura__lte=dto.data_fim)

        return qs

    @staticmethod
    def apply_global_search(qs, termo):
        if not termo:
            return qs

        q = Q()
        for p in termo.split():
            q |= (
                Q(motorista__nome__icontains=p) |
                Q(veiculo__prefixo__icontains=p)
            )
        return qs.filter(q)

    @staticmethod
    def apply_column_filters(qs, column_filters):
        if not column_filters:
            return qs

        for col, val in column_filters.items():
            field = COLUMN_MAP.get(col)
            if field and val:
                qs = qs.filter(**{f"{field}__icontains": val})

        return qs
    


def filtro_remocao(dto):
    q = Q(tipo_servico="Remoção")
   

    return q


def filtro_seletiva(dto):
    q = Q(tipo_servico="Seletiva")

    return q


def filtro_domiciliar(dto):
    q = Q(tipo_servico="Domiciliar")
    return q





