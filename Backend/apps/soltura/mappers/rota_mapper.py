from apps.soltura.models.rota import Rota
from apps.soltura.dto.rota_dtos import RotaDTO


class RotaMapper:
    @staticmethod
    def to_dto(model: Rota) -> RotaDTO:
        return RotaDTO(
            id_rota=model.id,
            pa=model.pa,
            rota=model.rota,
            tipo_servico=model.tipo_servico,
        )

    @staticmethod
    def to_dto_list(qs) -> list[RotaDTO]:
        return [RotaMapper.to_dto(obj) for obj in qs]
