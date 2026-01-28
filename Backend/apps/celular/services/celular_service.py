from django.db import transaction
from apps.celular.dto.celular_dto import CelularCreateDTO
from apps.celular.mappers.celular_mapper import CreateCelularMapper,CreateCelularResponseMapper
from apps.celular.models.celular import Celular
from apps.celular.utils.celular_utils import (
    validar_campos_obrigatorios,
    validar_numero_unico,
    validar_apelido_unico,
    validar_imei_unico,
)


class CelularCreateService:
    @staticmethod
    @transaction.atomic
    def execute(dto: CelularCreateDTO) -> Celular:
        validar_campos_obrigatorios(
            numero=dto.numero,
            apelido=dto.apelido,
            garagem_atual=dto.garagem_atual,
        )
        validar_numero_unico(dto.numero)
        validar_apelido_unico(dto.apelido)
        validar_imei_unico(dto.codigo_imei)
        celular = CreateCelularMapper.from_create_dto(dto)
        celular.save()
        return CreateCelularResponseMapper.from_model(celular)
