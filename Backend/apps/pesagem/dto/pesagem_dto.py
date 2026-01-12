from dataclasses import dataclass
from rest_framework.request import Request
from typing import List, Optional

@dataclass(frozen=True)
class CreatePesagemDTO:
    data: str
    prefixo_id: int
    colaborador_ids: List[int]
    cooperativa_id: int
    responsavel_coop: Optional[str]
    motorista_id: int
    hora_chegada: str
    hora_saida: str
    numero_doc: str
    volume_carga: str
    tipo_pesagem: str
    garagem: str
    turno: str


@dataclass(slots=True)
class PesagemListDTO:
    cursor: Optional[int]
    limit: 20
    start_date: Optional[str]
    end_date: Optional[str]
    tipo_pesagem: Optional[str]
    ordering: str = "id"

    @staticmethod
    def from_request(request: Request) -> "PesagemListDTO":
        return PesagemListDTO(
            cursor=int(request.query_params.get("cursor")) if request.query_params.get("cursor") else None,
            limit=min(int(request.query_params.get("limit", 20)), 100),
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
            tipo_pesagem=request.query_params.get("tipo_pesagem"),
            ordering=request.query_params.get("ordering") or "id",
        )
