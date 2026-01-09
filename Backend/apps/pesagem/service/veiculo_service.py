from apps.pesagem.dto.veiculo_dto import VeiculoListDTO,CreateVeiculoDTO,VeiculoContagemTipoDTO
from apps.pesagem.mappers.veiculos_mapper import VeiculoMapperList,VeiculoMapperCreate,VeiculosMapperTipo
from apps.pesagem.utils.cache_utils import get_cache, set_cache
from django.db import  transaction

##### cadastro de veiculos
class VeiculoServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: CreateVeiculoDTO) -> int:
        if VeiculoMapperCreate.exists_by_prefixo(dto.prefixo):
            raise ValueError("Prefixo já cadastrado")
        if VeiculoMapperCreate.exists_by_placa(dto.placa_veiculo):
            raise ValueError("Placa já cadastrada")
        return VeiculoMapperCreate.insert(dto)


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