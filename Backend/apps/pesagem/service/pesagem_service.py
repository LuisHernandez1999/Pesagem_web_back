from django.db import transaction
from apps.pesagem.dto.pesagem_dto import CreatePesagemDTO
from apps.pesagem.mappers.pesagem_mappers import PesagemMapperCreate,PesagemListMapper,PesagemTipoServicoMapper
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
    

class PesagemServiceList:
    @staticmethod
    def listar(dto):
        rows = PesagemListMapper.listar(dto)

        next_cursor = None
        if len(rows) > dto.limit:
            next_cursor = rows[-1]["id"]
            rows = rows[:-1]

        totais = PesagemListMapper.totais(dto)

        return {
            "results": rows,
            "next_cursor": next_cursor,
            **totais,
        }


class PesagemServiceListTipo:
    @staticmethod
    def total_seletiva() -> int:
        return PesagemTipoServicoMapper.total("SELETIVA")

    @staticmethod
    def total_cata_treco() -> int:
        return PesagemTipoServicoMapper.total("CATA-TRECO")