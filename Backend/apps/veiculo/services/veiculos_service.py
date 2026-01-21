from apps.veiculo.dto.veiculo_dto import VeiculoListDTO,VeiculoDTO,VeiculoContagemTipoDTO,VeiculoRankingDTO
from apps.veiculo.mappers.veiculos_mappers import VeiculoMapperList,VeiculoMapperCreate,VeiculosMapperTipo,RankingVeiculosPesagemMapper
from apps.pesagem.utils.cache_utils import get_cache, set_cache
from apps.veiculo.utils.veiculos_utils import validar_veiculo
from django.db import  transaction



##### cadastro de veiculos
class VeiculoServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: VeiculoDTO) -> int:
        validar_veiculo(dto)
        return VeiculoMapperCreate
        

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

        rows = VeiculoMapperList.listar(
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
            "veiculos": rows,
            "next_cursor": next_cursor,
        }

        set_cache(cache_key, result, timeout=30)
        return result


##### contagem por tipo 
class VeiculoServiceContagem:
    @staticmethod
    def contagem_por_tipo(dto: VeiculoContagemTipoDTO) -> dict:
        cache_key = f"veiculo_contagem_tipo:{dto.tipo_servico}"

        cached = get_cache(cache_key)
        if cached:
            return cached

        total, ativos, inativos = VeiculosMapperTipo.contagem_por_tipo(
            dto.tipo_servico
        )

        result = {
            "tipo_servico": dto.tipo_servico,
            "total": total,
            "ativos": ativos,
            "inativos": inativos,
        }

        set_cache(cache_key, result, timeout=120)
        return result
    



class VeiculoRankingService:
    @staticmethod
    def get(dto: VeiculoRankingDTO) -> int:
        return RankingVeiculosPesagemMapper.get(dto)