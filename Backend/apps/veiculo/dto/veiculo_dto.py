from dataclasses import dataclass
from typing import Optional
from rest_framework.request import Request



@dataclass(frozen=True, slots=True)
class CreateVeiculoDTO:
    prefixo: str
    tipo_veiculo: str
    placa_veiculo: Optional[str]
    em_manutencao: str
    status: str
    tipo_servico: str
    equipamento: str


@dataclass(slots=True)
class VeiculoListDTO:
    cursor: int
    search: Optional[str]
    ordering: str
    limit: int = 20
    @classmethod
    def from_request(cls, request) -> "VeiculoListDTO":
        query = request.query_params
        return cls(
            cursor=int(query.get("cursor")) if query.get("cursor") else None,
            search=query.get("search"),
            ordering=query.get("ordering", "id"),
            limit=int(query.get("limit", 20)),
        )


class VeiculoContagemTipoDTO:
    tipo_servico: str
    @staticmethod
    def from_request(request: Request) -> "VeiculoContagemTipoDTO":
        tipo_servico = request.query_params.get("tipo_servico")
        if not tipo_servico:
            raise ValueError("tipo_servico é obrigatório")
        return VeiculoContagemTipoDTO(
            tipo_servico=tipo_servico
        )
    


class VeiculoRankingDTO:
    cursor: int
    search: Optional[str]
    ordering: str
    limit: int = 20
    @classmethod
    def from_request(cls, request) -> "VeiculoListDTO":
        query = request.query_params
        return cls(
            cursor=int(query.get("cursor")) if query.get("cursor") else None,
            search=query.get("search"),
            ordering=query.get("ordering", "id"),
            limit=int(query.get("limit", 20)),
        )
