from django.db.models import Q

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





