from django.db import transaction
from apps.cooperativa.dto.cooperativa_dto import CreateCooperativaDTO,CooperativaEficienciaDTO
from apps.cooperativa.mappers.cooperativa_mappers import CooperativaMapperCreate,CooperativaEficienciaMapper
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
    


class CooperativaEfcinenciaService():
    @staticmethod
    def get(dto:CooperativaEficienciaDTO) ->int:
        return CooperativaEficienciaMapper.get(dto)
    


    


