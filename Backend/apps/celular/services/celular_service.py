from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.celular.dto.celular_dto import (CelularCreateDTO,CelularListResponseDTO,CelularListRequestDTO
                                          ,CelularDeleteResponseDTO,CelularDeleteRequestDTO,
                                          CelularUpdateRequestDTO,CelularUpdateResponseDTO)
from apps.celular.mappers.celular_mapper import (CreateCelularMapper,CreateCelularResponseMapper,
                                                 ListCelularMapper,CelularDeleteMapper,CelularUpdateMapper)
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


class CelularListService:
    @staticmethod
    def listar_celulares(dto: CelularListRequestDTO) -> CelularListResponseDTO:
        cursor = dto.cursor or 0

        qs = (
            Celular.objects
            .filter(id__gt=cursor)
            .order_by("id")
        )
        celulares = list(qs[:11])   
        has_next = len(celulares) > 10
        page = celulares[:10]
        next_cursor = page[-1].id if has_next else None
        return CelularListResponseDTO(
            results=[ListCelularMapper.from_model(c) for c in page],
            next_cursor=next_cursor,
            has_next=has_next,
        )
    

class CelularDeleteService:
    @staticmethod
    @transaction.atomic
    def delete(dto: CelularDeleteRequestDTO) -> CelularDeleteResponseDTO:
        celular = get_object_or_404(Celular, id=dto.celular_id)
        celular.delete()
        return CelularDeleteMapper.success_response()
    

class CelularUpdateService:
    @staticmethod
    @transaction.atomic
    def update(dto: CelularUpdateRequestDTO) -> CelularUpdateResponseDTO:
        celular = get_object_or_404(Celular, id=dto.celular_id)
        if dto.numero and dto.numero != celular.numero:
            validar_numero_unico(dto.numero)
            celular.numero = dto.numero
        if dto.apelido and dto.apelido != celular.apelido:
            validar_apelido_unico(dto.apelido)
            celular.apelido = dto.apelido
        if dto.codigo_imei and dto.codigo_imei != celular.codigo_imei:
            validar_imei_unico(dto.codigo_imei)
            celular.codigo_imei = dto.codigo_imei
        for field in [
            "ativo",
            "modelo",
            "fabricante",
            "garagem_atual",
        ]:
            value = getattr(dto, field)
            if value is not None:
                setattr(celular, field, value)
        celular.save()
        return CelularUpdateMapper.from_model(celular)