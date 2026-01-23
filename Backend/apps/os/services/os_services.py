from django.db import transaction
from typing import List, Optional, Tuple
from apps.os.models import OrdemServico
from apps.os.dto.os_dto import OrdemServicoCreateDTO,OrdemServicoListFilterDTO
from apps.os.mappers.os_mappers import OrdemServicoMapperCreate,OrdemServicoVisualizacaoMapper
from apps.os.utils.os_utils import validar_os_create


class OrdemServicoServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: OrdemServicoCreateDTO):
        validar_os_create(dto)
        return OrdemServicoMapperCreate.insert(dto)



class OrdemServicoVisualizacaoService:
    @staticmethod
    def listar(dto: OrdemServicoListFilterDTO):
        return OrdemServicoVisualizacaoMapper.listar(dto)