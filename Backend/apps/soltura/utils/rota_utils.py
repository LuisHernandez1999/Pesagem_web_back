from django.core.exceptions import ValidationError
from apps.soltura.models.rota import Rota


def validar_campos_obrigatorios(pa: str, rota: str, tipo_servico: str) -> None:
    if not pa:
        raise ValidationError("PA é obrigatório")
    if not rota:
        raise ValidationError("Rota é obrigatória")
    if not tipo_servico:
        raise ValidationError("Tipo de serviço é obrigatório")


def validar_rota_unica(pa: str, rota: str, tipo_servico: str) -> None:
    if Rota.objects.filter(
        pa=pa,
        rota=rota,
        tipo_servico=tipo_servico
    ).exists():
        raise ValidationError("Já existe rota cadastrada com esses dados")
