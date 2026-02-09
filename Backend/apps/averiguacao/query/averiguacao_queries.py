import datetime
from django.db.models import F, Case, When, CharField, Count
from apps.averiguacao.models.averiguacao import Averiguacao

class AveriguacaoQuery:

    @staticmethod
    def buscar_averiguacoes(pa=None, turno=None, servico=None, dia_semana=None, cursor=None, direction="next", limit=50, data_inicio=None, data_fim=None):
        query = Averiguacao.objects.select_related(
            "rota_averiguada", "rota_averiguada__rota", "rota_averiguada__setor"
        )

        # Filtro por datas
        if data_inicio and data_fim:
            query = query.filter(data__range=[data_inicio, data_fim])

        # Filtro por múltiplos PAs
        if pa:
            if isinstance(pa, list):
                query = query.filter(pa_da_averiguacao__in=pa)
            else:
                query = query.filter(pa_da_averiguacao=pa)

        if servico:
            query = query.filter(tipo_servico=servico)
        if turno:
            query = query.filter(rota_averiguada__turno=turno)

        # filtro por dia da semana
        dias_map = {"domingo": 1, "segunda": 2, "terça": 3, "terca": 3,
                    "quarta": 4, "quinta": 5, "sexta": 6, "sábado": 7, "sabado": 7}
        if dia_semana:
            chave = dia_semana.strip().lower()
            if chave in dias_map:
                query = query.filter(rota_averiguada__data_soltura__week_day=dias_map[chave])

        # annotate rota_nome
        query = query.annotate(
            rota_nome=Case(
                When(rota_averiguada__rota__isnull=False, then=F("rota_averiguada__rota__rota")),
                default=F("rota_averiguada__setor__nome_setor"),
                output_field=CharField()
            )
        ).order_by("-id")

        if cursor:
            if direction == "next":
                query = query.filter(id__lt=cursor)
            elif direction == "prev":
                query = query.filter(id__gt=cursor).order_by("id")

        registros = list(query[:limit + 1])
        if direction == "prev":
            registros = list(reversed(registros))

        return registros, query.count()
