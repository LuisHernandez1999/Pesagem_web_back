import datetime
from dataclasses import fields
from django.utils import timezone
from dataclasses import fields
from typing import get_origin, get_args, Union
PA_ESTABELECIDAS = ("PA1", "PA2", "PA3", "PA4")

METAS_SEMANAIS = {
    "Remoção": 120,
    "Domiciliar": 100,
    "Seletiva": 90,
}



def validar_campos_obrigatorios(dto) -> None:
    faltantes = []

    for field in fields(dto):
        tipo = field.type
        valor = getattr(dto, field.name)

        is_optional = (
            get_origin(tipo) is Union and type(None) in get_args(tipo)
        )

        if not is_optional and valor is None:
            faltantes.append(field.name)

    if faltantes:
        raise ValueError(
            f"Campos obrigatórios ausentes: {', '.join(faltantes)}"
        )

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


def validar_obrigatorios_por_dto(dto) -> None:
    faltantes = [
        field.name
        for field in fields(dto)
        if getattr(dto, field.name) is None
    ]

    if faltantes:
        raise ValueError(
            f"Campos obrigatórios ausentes: {', '.join(faltantes)}"
        )