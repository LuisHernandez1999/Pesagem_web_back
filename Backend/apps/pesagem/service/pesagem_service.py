from django.db import transaction
from apps.pesagem.utils.pesagem_utils import validar_pesagem
from apps.pesagem.dto.pesagem_dto import CreatePesagemDTO,PesagemListDTO,ExibirPesagemPorMesDTO,PesagemCreateDocDTO
from apps.pesagem.mappers.pesagem_mappers import (PesagemMapperCreate,
                                                  PesagemListMapper,PesagemTipoServicoMapper,
                                                  ExibirPesagemPorMesMapper,
                                                  PesagemQuantidadeMapper,
                                                  PesagemGerarDocMapper)


class PesagemServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: CreatePesagemDTO) -> int:
        validar_pesagem(dto)
        pesagem_id = PesagemMapperCreate.insert(dto)
        return pesagem_id
    

class PesagemListService:
    @staticmethod
    def execute(dto:PesagemListDTO):
        rows, next_cursor = PesagemListMapper.list(dto)
        return {
            "results": rows,
            "next_cursor": next_cursor,
            
        }

class ExibirPesagemPorMesService:
    @staticmethod
    def execute(dto:ExibirPesagemPorMesDTO):
        data = ExibirPesagemPorMesMapper.fetch(dto)

        return {
            "pesagens_por_periodo_personalizado": data
        }


class PesagemTotalService:
    @staticmethod
    def total_pesagem() -> int:
        return PesagemQuantidadeMapper
    


class PesagemServiceListTipo:
    @staticmethod
    def total_seletiva() -> int:
        return PesagemTipoServicoMapper.total("SELETIVA")
    @staticmethod
    def total_cata_treco() -> int:
        return PesagemTipoServicoMapper.total("CATA-TRECO")
    


class PesagemServiceDoc:
    @staticmethod
    def executar(dto: PesagemCreateDocDTO) -> list[dict]:
        return PesagemGerarDocMapper.get(dto)

