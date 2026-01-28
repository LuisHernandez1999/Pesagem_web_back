from django.db import transaction
from  apps.confirmacao.mappers.confiramcao_mappers import ConfirmacaoCreateMapper
from apps.confirmacao.utils.confirmacao_utils import validar_confirmacao


class ConfirmacaoServicoCreateService:

    @staticmethod
    @transaction.atomic
    def executar(dto):
        validar_confirmacao(dto)
        return ConfirmacaoCreateMapper.criar(dto)
