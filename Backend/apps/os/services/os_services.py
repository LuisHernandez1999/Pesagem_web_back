from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from apps.os.models import OrdemServico
from apps.veiculo.models import Veiculo
from apps.os.dto.os_dto import OrdemServicoCreateDTO


class OrdemServicoService:

    @staticmethod
    @transaction.atomic
    def criar(dto: OrdemServicoCreateDTO) -> OrdemServico:

        # ===== validações =====
        if not dto.pa:
            raise ValidationError("pa é obrigatório")

        if not dto.os_numero:
            raise ValidationError("os_numero é obrigatório")

        if not dto.veiculo_prefixo:
            raise ValidationError("veiculo_prefixo é obrigatório")

        # ===== buscar veículo por prefixo =====
        try:
            veiculo = Veiculo.objects.get(prefixo=dto.veiculo_prefixo)
        except Veiculo.DoesNotExist:
            raise ValidationError("Veículo não encontrado para o prefixo informado")

        # ===== inicio_problema =====
        inicio = dto.inicio_problema
        if isinstance(inicio, str):
            inicio = parse_datetime(inicio)

        if not inicio:
            raise ValidationError("inicio_problema inválido")

        if timezone.is_naive(inicio):
            inicio = timezone.make_aware(inicio)

        # ===== conclusao (opcional) =====
        conclusao = dto.conclusao
        if conclusao:
            if isinstance(conclusao, str):
                conclusao = parse_datetime(conclusao)

            if not conclusao:
                raise ValidationError("conclusao inválida")

            if timezone.is_naive(conclusao):
                conclusao = timezone.make_aware(conclusao)

        # ===== regra: OS aberta =====
        if not conclusao and OrdemServico.objects.filter(
            veiculo=veiculo,
            conclusao__isnull=True
        ).exists():
            raise ValidationError("Este veículo já possui uma OS em aberto")

        # ===== criar =====
        return OrdemServico.objects.create(
            pa=dto.pa,
            os_numero=dto.os_numero,
            veiculo=veiculo,
            inicio_problema=inicio,
            conclusao=conclusao
        )
