from apps.averiguacao.mappers.averiguacao_mapper import AveriguacaoCreateMapper
from apps.averiguacao.dto.averiguacao_dto import AveriguacaoCreateDTO
from django.db import transaction

class AveriguacaoServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: AveriguacaoCreateDTO) -> int:
        return AveriguacaoCreateMapper.insert(dto)
    


