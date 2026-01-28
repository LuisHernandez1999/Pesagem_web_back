from django.core.exceptions import ValidationError
from apps.veiculo.models import Veiculo
from apps.colaborador.models import Colaborador


def validar_motorista(motorista):
    if motorista.status != "ATIVO":
        raise ValidationError("Motorista inativo")


def validar_veiculo(veiculo: Veiculo):
    if veiculo.em_manutencao.upper() != "NÃO":
        raise ValidationError("Veículo em manutenção")


def validar_coletores(coletores, tipo_servico):
    if tipo_servico in ["Seletiva", "Domiciliar"] and not coletores:
        raise ValidationError(f"{tipo_servico} exige coletores")

    if tipo_servico == "Varrição" and coletores:
        raise ValidationError("Varrição não deve ter coletores")
