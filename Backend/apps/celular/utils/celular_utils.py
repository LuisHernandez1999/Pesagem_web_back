from apps.celular.models.celular import Celular
from apps.celular.exceptions.celular_exceptions import (
    CelularCampoObrigatorio,
    CelularNumeroDuplicado,
    CelularApelidoDuplicado,
    CelularImeiDuplicado,
)


def validar_campos_obrigatorios(**campos):
    for nome, valor in campos.items():
        if valor is None or valor == "":
            raise CelularCampoObrigatorio(nome)


def validar_numero_unico(numero: str):
    if Celular.objects.filter(numero=numero).exists():
        raise CelularNumeroDuplicado()


def validar_apelido_unico(apelido: str):
    if Celular.objects.filter(apelido=apelido).exists():
        raise CelularApelidoDuplicado()


def validar_imei_unico(codigo_imei: str | None):
    if codigo_imei and Celular.objects.filter(codigo_imei=codigo_imei).exists():
        raise CelularImeiDuplicado()
