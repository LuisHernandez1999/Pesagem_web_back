import datetime
from django.utils import timezone

PA_ESTABELECIDAS = ("PA1", "PA2", "PA3", "PA4")

METAS_SEMANAIS = {
    "Remoção": 120,
    "Domiciliar": 100,
    "Seletiva": 90,
}


def calcular_periodo_semana(data_inicio=None, data_fim=None):
    hoje = timezone.localdate()

    if data_inicio and data_fim:
        return (
            datetime.date.fromisoformat(data_inicio),
            datetime.date.fromisoformat(data_fim),
        )

    inicio = hoje - datetime.timedelta(days=hoje.weekday())
    fim = inicio + datetime.timedelta(days=6)
    return inicio, fim
