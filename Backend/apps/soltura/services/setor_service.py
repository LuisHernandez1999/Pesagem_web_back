from django.db import transaction
from apps.soltura.mappers.setor_mapper import SetorMapperCreate,SetorMapper
from apps.soltura.dto.setor_dtos  import SetorCreateDTO, SetorResponseDTO
from apps.soltura.models.setor import Setor
class SetorServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: SetorCreateDTO) -> int:
        setor_id = SetorMapperCreate.insert(dto)
        return setor_id
    
class SetorGetService:
    @staticmethod
    def execute(setor_id: int) -> SetorResponseDTO | None:
        try:
            setor = Setor.objects.get(pk=setor_id)
            return SetorMapper.to_dto(setor)
        except Setor.DoesNotExist:
            return None

class SetorUpdateService:
    @staticmethod
    def execute(setor_id: int, dto: SetorCreateDTO) -> SetorResponseDTO | None:
        try:
            setor = Setor.objects.get(pk=setor_id)
            setor.nome_setor = dto.nome_setor
            setor.regiao = dto.regiao
            setor.save()
            return SetorMapper.to_dto(setor)
        except Setor.DoesNotExist:
            return None
        
class SetorDeleteService:
    @staticmethod
    def execute(setor_id: int) -> bool:
        deleted, _ = Setor.objects.filter(pk=setor_id).delete()
        return deleted > 0
    
class SetorListService:
    @staticmethod
    def execute(last_id: int = None, limit: int = 10) -> list[SetorResponseDTO]:
        query = Setor.objects.all().order_by("id")
        if last_id:
            query = query.filter(id__gt=last_id)
        return [SetorMapper.to_dto(s) for s in query[:limit]]