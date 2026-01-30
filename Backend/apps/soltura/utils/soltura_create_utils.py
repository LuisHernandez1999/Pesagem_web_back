from django.core.exceptions import ValidationError
from apps.veiculo.models import Veiculo
from apps.colaborador.models import Colaborador



def validar_soltura(dto):
    validar_veiculo(dto)
    validar_motorista(dto)
    validar_coletores(dto)


def validar_veiculo(dto):
    veiculo = Veiculo.objects.filter(id=dto.veiculo_id).first()
    if not veiculo:
        raise ValidationError("Veículo não encontrado")

    if veiculo.em_manutencao == "SIM":
        raise ValidationError("Veículo em manutenção")

    if veiculo.tipo_servico.lower() != dto.tipo_servico.lower():
        raise ValidationError("Veículo incompatível com o tipo de serviço")
def validar_motorista(dto):
    motorista = Colaborador.objects.filter(
        id=dto.motorista_id,
        funcao__in=["MOTORISTA", "OPERADOR"],
        status="ATIVO",
        pa=dto.garagem   
    ).first()

    if not motorista:
        raise ValidationError("Motorista inválido")


def validar_coletores(dto):
    if dto.tipo_servico.lower() in ["seletiva", "domiciliar"]:
        if not dto.coletores_ids:
            raise ValidationError("Este tipo de serviço exige coletores")

        qs = Colaborador.objects.filter(
            id__in=dto.coletores_ids,
            funcao="COLETOR",
            status="ATIVO",
            pa=dto.garagem   
        )

        if qs.count() != len(dto.coletores_ids):
            raise ValidationError("Coletores inválidos")