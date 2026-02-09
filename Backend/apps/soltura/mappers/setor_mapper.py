from apps.soltura.dto.setor_dtos import SetorCreateDTO,SetorResponseDTO
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
    


class SetorMapper:

    @staticmethod
    def to_model(dto: SetorCreateDTO) -> Setor:
        return Setor(
            nome_setor=dto.nome_setor,
            regiao=dto.regiao
        )

    @staticmethod
    def to_dto(model: Setor) -> SetorResponseDTO:
        return SetorResponseDTO(
            id=model.id,
            nome_setor=model.nome_setor,
            regiao=model.regiao
        )



