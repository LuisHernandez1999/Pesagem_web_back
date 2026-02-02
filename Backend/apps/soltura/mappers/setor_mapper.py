from apps.soltura.dto.setor_dtos import SetorCreateDTO
from apps.soltura.models.setor import Setor


class SetorMapperCreate:
    @staticmethod
    def insert(model:Setor) -> SetorCreateDTO:
        return SetorCreateDTO(
            id_setor=model.id,
            nome_setor=model.nome_setor,
            regiao=model.regiao
        )
    @staticmethod
    def to_dto_list(qs) -> list[SetorCreateDTO]:
        return [SetorMapperCreate.to_dto(obj) for obj in qs]



