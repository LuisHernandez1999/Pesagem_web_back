from apps.celular.dto.celular_dto import (CelularCreateDTO,CelularCreateResponseDTO,
                                          CelularListDTO,CelularDeleteResponseDTO,
                                          CelularUpdateRequestDTO,CelularUpdateResponseDTO)
from apps.celular.models.celular import Celular

class CreateCelularMapper:
    @staticmethod
    def from_create_dto(dto:CelularCreateDTO) -> Celular:
        return Celular(
               numero= dto.numero,
               ativo=dto.ativo,
               modelo=dto.modelo,
               fabricante=dto.fabricante,
               garagem_atual=dto.garagem_atual,
               codigo_imei=dto.codigo_imei,
               apelido=dto.apelido
        )
    

class CreateCelularResponseMapper:
    @staticmethod
    def from_model(model: Celular) -> CelularCreateResponseDTO:
        return CelularCreateResponseDTO(
            id=model.id,
            numero=model.numero,
            ativo=model.ativo,
            modelo=model.modelo,
            fabricante=model.fabricante,
            garagem_atual=model.garagem_atual,
            codigo_imei=model.codigo_imei,
            apelido=model.apelido,
        )
    


class ListCelularMapper:
    @staticmethod
    def from_model(celular: Celular) -> CelularListDTO:
        return CelularListDTO(
            numero=celular.numero,
            ativo=celular.ativo,
            modelo=celular.modelo,
            fabricante=celular.fabricante,
            garagem_atual=celular.garagem_atual,
            codigo_imei=celular.codigo_imei,
            apelido=celular.apelido,
        )



class CelularDeleteMapper:
    @staticmethod
    def success_response() -> CelularDeleteResponseDTO:
        return CelularDeleteResponseDTO(
            message="Celular removido com sucesso."
        )
    

class CelularUpdateMapper:
    @staticmethod
    def from_model(celular: Celular) -> CelularUpdateResponseDTO:
        return CelularUpdateResponseDTO(
            id=celular.id,
            numero=celular.numero,
            ativo=celular.ativo,
            modelo=celular.modelo,
            fabricante=celular.fabricante,
            garagem_atual=celular.garagem_atual,
            codigo_imei=celular.codigo_imei,
            apelido=celular.apelido,
        )