from apps.colaborador.dto.colaborador_dto import ColaboradorListDTO
from apps.colaborador.mappers.colaborador_mappers import ColaboradorMapperList
from apps.pesagem.utils.cache_utils import get_cache, set_cache
from django.db import transaction,IntegrityError
from apps.colaborador.dto.colaborador_dto import CreateColaboradorDTO
from apps.colaborador.utils.colaborador_utils import validar_colaborador
from apps.colaborador.mappers.colaborador_mappers import ColaboradorMapperCreate
from apps.colaborador.exceptions.colaborador_exceptions import (
    MatriculaAlreadyExists,
)


class ColaboradorServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: CreateColaboradorDTO) -> int:
        validar_colaborador(dto)
        try:
            return ColaboradorMapperCreate.insert(dto)
        except IntegrityError:
            raise MatriculaAlreadyExists()

class ColaboradorServiceList:
    @staticmethod
    def listar(dto: ColaboradorListDTO):
        cache_key = f"colaborador:{dto.cursor}:{dto.limit}:{dto.funcao}:{dto.turno}:{dto.ordering}"

        cached = get_cache(cache_key)
        if cached:
            return cached

        rows = ColaboradorMapperList.listar(
            cursor=dto.cursor,
            limit=dto.limit + 1,
            funcao=dto.funcao,
            turno=dto.turno,
            ordering=dto.ordering
        )

        next_cursor = None
        if len(rows) > dto.limit:
            next_cursor = rows[-1]["id"]
            rows = rows[:-1]

        result = {
            "results": rows,
            "next_cursor": next_cursor,
        }

        set_cache(cache_key, result, timeout=30)
        return result
