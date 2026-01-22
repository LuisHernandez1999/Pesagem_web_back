from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from apps.movimentacao.models import Movimentacao
from apps.os.models import OrdemServico
from apps.colaborador.models import Colaborador
from apps.movimentacao.dto.movimentacao_dto import MovimentacaoCreateDTO


class MovimentacaoService:

    @staticmethod
    @transaction.atomic
    def criar(dto: MovimentacaoCreateDTO) -> Movimentacao:

        # ===== OS =====
        try:
            os = OrdemServico.objects.get(id=dto.os_id)
        except OrdemServico.DoesNotExist:
            raise ValidationError("Ordem de Serviço não encontrada")

        # ===== responsável (pela matrícula) =====
        try:
            responsavel = Colaborador.objects.get(
                matricula=dto.responsavel_matricula
            )
        except Colaborador.DoesNotExist:
            raise ValidationError("Colaborador não encontrado pela matrícula")

        # ===== data_hora =====
        data_hora = dto.data_hora
        if isinstance(data_hora, str):
            data_hora = parse_datetime(data_hora)

        if not data_hora:
            raise ValidationError("data_hora inválida ou obrigatória")

        if timezone.is_naive(data_hora):
            data_hora = timezone.make_aware(data_hora)

        # ===== status =====
        if not dto.status:
            raise ValidationError("status é obrigatório")

        # ===== criar movimentação =====
        return Movimentacao.objects.create(
            os=os,
            data_hora=data_hora,
            status=dto.status,
            responsavel=responsavel,
            observacao=dto.observacao
        )
