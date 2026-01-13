from django.db import transaction
from apps.pesagem.dto.pesagem_dto import CreatePesagemDTO
from apps.pesagem.mappers.pesagem_mappers import PesagemMapperCreate,PesagemListMapper,PesagemTipoServicoMapper,ExibirPesagemPorMesMapper
from apps.pesagem.utils.pesagem_utils import validar_pesagem

class PesagemServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: CreatePesagemDTO) -> int:
        # Valida dados da pesagem antes de criar
        validar_pesagem(dto)
        # Cria a pesagem e vincula colaboradores diretamente no mapper
        pesagem_id = PesagemMapperCreate.insert(dto)
        # Removida a chamada para vincular_colaboradores inexistente
        return pesagem_id
    

class PesagemListService:
    @staticmethod
    def execute(dto):
        rows, next_cursor = PesagemListMapper.list(dto)
        return {
            "results": rows,
            "next_cursor": next_cursor,
            
        }

class ExibirPesagemPorMesService:
    @staticmethod
    def execute(dto):
        data = ExibirPesagemPorMesMapper.fetch(dto)

        return {
            "pesagens_por_periodo_personalizado": data
        }


class PesagemServiceListTipo:
    @staticmethod
    def total_seletiva() -> int:
        return PesagemTipoServicoMapper.total("SELETIVA")

    @staticmethod
    def total_cata_treco() -> int:
        return PesagemTipoServicoMapper.total("CATA-TRECO")