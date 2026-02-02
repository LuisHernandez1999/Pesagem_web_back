from django.db import transaction
from apps.soltura.mappers.setor_mapper import SetorMapperCreate
from apps.soltura.dto.setor_dtos  import SetorCreateDTO
class SetorServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: SetorCreateDTO) -> int:
        setor_id = SetorMapperCreate.insert(dto)
        return setor_id
    



