from django.utils import timezone
from django.utils.dateparse import parse_datetime

from apps.movimentacao.dto.movimentacao_dto import MovimentacaoCreateDTO
from apps.movimentacao.constants.status import STATUS_MOVIMENTACAO
from apps.movimentacao.exceptions.movimentacao_exceptions  import (
    CampoObrigatorio,
    StatusMovimentacaoInvalido,
    DataHoraInvalida,
)


def validar_movimentacao_create(dto: MovimentacaoCreateDTO):

    if not dto.os_numero:
        raise CampoObrigatorio("os_numero")

    if not dto.responsavel_matricula:
        raise CampoObrigatorio("responsavel_matricula")

    if not dto.status:
        raise CampoObrigatorio("status")

    if dto.status not in STATUS_MOVIMENTACAO:
        raise StatusMovimentacaoInvalido(dto.status)

    # ===== data_hora =====
    data_hora = dto.data_hora

    if isinstance(data_hora, str):
        data_hora = parse_datetime(data_hora)

    if not data_hora:
        raise DataHoraInvalida()

    if timezone.is_naive(data_hora):
        data_hora = timezone.make_aware(data_hora)

    dto.data_hora = data_hora