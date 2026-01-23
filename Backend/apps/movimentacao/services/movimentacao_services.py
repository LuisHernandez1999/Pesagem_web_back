from django.db import transaction
from apps.movimentacao.dto.movimentacao_dto import MovimentacaoCreateDTO,MovimentacaoListCursorDTO
from apps.movimentacao.mappers.movimentacao_mappers import MovimentacaoMapperCreate
from apps.movimentacao.utils.movimentacao_utils import validar_movimentacao_create
from apps.movimentacao.mappers.movimentacao_mappers import MovimentacaoMapperList


class MovimentacaoServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: MovimentacaoCreateDTO):
        validar_movimentacao_create(dto)
        return MovimentacaoMapperCreate.insert(dto)




class MovimentacaoListService:
    @staticmethod
    def listar_com_cursor(dto: MovimentacaoListCursorDTO):
        return MovimentacaoMapperList.listar_com_cursor(dto)
