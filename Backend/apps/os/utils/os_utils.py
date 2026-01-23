from django.utils import timezone
from django.utils.dateparse import parse_datetime

from apps.os.exceptions.os_exceptions import (
    PaObrigatorio,
    OsNumeroObrigatorio,
    VeiculoPrefixoObrigatorio,
    InicioProblemaInvalido,
    ConclusaoInvalida,

    
)


def validar_os_create(dto):

    if not dto.pa:
        raise PaObrigatorio("pa é obrigatório")

    if not dto.os_numero:
        raise OsNumeroObrigatorio("os_numero é obrigatório")

    if not dto.veiculo_prefixo:
        raise VeiculoPrefixoObrigatorio("veiculo_prefixo é obrigatório")

    inicio = dto.inicio_problema
    if isinstance(inicio, str):
        inicio = parse_datetime(inicio)

    if not inicio:
        raise InicioProblemaInvalido("inicio_problema inválido")

    if timezone.is_naive(inicio):
        inicio = timezone.make_aware(inicio)

    dto.inicio_problema = inicio

    if dto.conclusao:
        conclusao = dto.conclusao
        if isinstance(conclusao, str):
            conclusao = parse_datetime(conclusao)

        if not conclusao:
            raise ConclusaoInvalida("conclusao inválida")

        if timezone.is_naive(conclusao):
            conclusao = timezone.make_aware(conclusao)

        dto.conclusao = conclusao







