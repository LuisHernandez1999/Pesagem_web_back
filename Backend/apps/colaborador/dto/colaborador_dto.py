from dataclasses import dataclass
from typing import Optional
from rest_framework.request import Request


@dataclass(frozen=True)
class CreateColaboradorDTO:
    nome: str
    matricula: int
    funcao: str
    turno: str
    status: str
    pa: str


@dataclass(slots=True)
class ColaboradorListDTO:
    cursor: int 
    limit: 20
    funcao: Optional[str]
    turno: Optional[str]
    pa:Optional[str]
    ordering:Optional [str]

    @staticmethod
    def from_request(request: Request) -> "ColaboradorListDTO":
      return ColaboradorListDTO(
        cursor=(
            int(request.query_params.get("cursor"))
            if request.query_params.get("cursor")
            else None
        ),
        limit=min(int(request.query_params.get("limit", 20)), 100),
        funcao=request.query_params.get("funcao"),
        turno=request.query_params.get("turno"),
        pa=request.query_params.get("pa"),
        ordering=request.query_params.get("ordering") or "id",
    )

@dataclass(slots=True)
class ColaboradorListItemDTO:
    id: int
    nome: str
    matricula: str
    funcao: str
    turno: str
    status: str
    pa: str

