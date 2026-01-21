from django.db import transaction
from django.core.exceptions import ValidationError
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
        if OrdemServico.objects.filter(os_numero=dto.os_numero).exists():
            raise ValidationError("Já existe uma OS com esse número")
        if OrdemServico.objects.filter(
            veiculo=veiculo,
            conclusao__isnull=True
        ).exists():
            raise ValidationError(
                "Este veículo já possui uma OS em aberto"
            )

        os = OrdemServico.objects.create(
            pa=dto.pa,
            os_numero=dto.os_numero,
            veiculo=veiculo,
            inicio_problema=dto.inicio_problema
        )

        return os
