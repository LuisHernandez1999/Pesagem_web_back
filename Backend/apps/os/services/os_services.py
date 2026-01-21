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

        try:
            veiculo = Veiculo.objects.get(id=dto.veiculo_id)
        except Veiculo.DoesNotExist:
            raise ValidationError("Veículo não encontrado")

        # ===== parse datetime =====
        inicio_problema = dto.inicio_problema

        if isinstance(inicio_problema, str):
            inicio_problema = parse_datetime(inicio_problema)

        if not inicio_problema:
            raise ValidationError("inicio_problema é obrigatório")

        if timezone.is_naive(inicio_problema):
            inicio_problema = timezone.make_aware(inicio_problema)

        # ===== regra: uma OS aberta por veículo =====
        if OrdemServico.objects.filter(
            veiculo=veiculo,
            conclusao__isnull=True
        ).exists():
            raise ValidationError(
                "Este veículo já possui uma OS em aberto"
            )

        # ===== gerar número da OS =====
        os_numero = timezone.now().strftime("%Y%m%d%H%M%S%f")

        os = OrdemServico.objects.create(
            pa=dto.pa,
            os_numero=os_numero,
            veiculo=veiculo,
            inicio_problema=inicio_problema
        )

        return os
