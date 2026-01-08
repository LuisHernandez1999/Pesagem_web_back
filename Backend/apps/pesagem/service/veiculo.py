from apps.pesagem.dto.veiculo_dto import VeiculoListDTO
from apps.pesagem.mappers.veiculos_mapper import VeiculoMapper
from apps.pesagem.utils.cache_utils import get_cache, set_cache


class VeiculoServiceList:
    @staticmethod
    def listar(dto: VeiculoListDTO):
        cache_key = (
            f"veiculos:"
            f"{dto.cursor}:"
            f"{dto.limit}:"
            f"{dto.search}:"
            f"{dto.ordering}"
        )
        cached = get_cache(cache_key)
        if cached:
            return cached

        rows = VeiculoMapper.listar(
            cursor=dto.cursor,
            limit=dto.limit + 1,
            search=dto.search,
            ordering=dto.ordering,
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
    @staticmethod
    def contagem(tipo_servico: str):
        cache_key = f"veiculo_contagem:{tipo_servico}"

        cached = get_cache(cache_key)
        if cached:
            return cached

        total, ativos, inativos = VeiculoMapper.contagem_por_tipo(tipo_servico)

        result = {
            "total": total,
            "ativos": ativos,
            "inativos": inativos,
        }

        set_cache(cache_key, result, timeout=120)
        return result
