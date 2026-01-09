from apps.pesagem.dto.colaborador_dto import ColaboradorListDTO
from apps.pesagem.mappers.colaborador_mapper import ColaboradorMapperList
from apps.pesagem.utils.cache_utils import get_cache, set_cache
from django.db import transaction,IntegrityError
from apps.pesagem.dto.colaborador_dto import CreateColaboradorDTO
from apps.pesagem.utils.colaborador_utils import validar_colaborador
from apps.pesagem.mappers.colaborador_mapper import ColaboradorMapperCreate
from apps.pesagem.exceptions.colaborador_exceptions import (
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
        cache_key = f"colaborador:{dto.cursor}:{dto.limit}:{dto.funcao}:{dto.turno}"

        cached = get_cache(cache_key)
        if cached:
            return cached

        rows = ColaboradorMapperList.listar(
            cursor=dto.cursor,
            limit=dto.limit + 1,
            funcao=dto.funcao,
            turno=dto.turno,
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
