from django.db import transaction
from apps.cooperativa.dto.cooperativa_dto import CreateCooperativaDTO
from apps.cooperativa.mappers.cooperativa_mappers import CooperativaMapperCreate
from apps.cooperativa.excepetions.cooperativa_exceptions import (
    CooperativaAlreadyExists,
)


class CreateCooperativaService:
    @staticmethod
    @transaction.atomic
    def create(dto: CreateCooperativaDTO) -> int:
        if CooperativaMapperCreate.exists_by_nome(dto.nome):
            raise CooperativaAlreadyExists()
        return CooperativaMapperCreate.insert(dto)
    


