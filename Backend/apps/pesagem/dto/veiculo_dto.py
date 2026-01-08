from dataclasses import dataclass
from rest_framework.request import Request


@dataclass(slots=True)
class VeiculoListDTO:
    cursor: int | None
    limit: int
    search: str | None
    ordering: str
    @staticmethod
    def from_request(request: Request) -> "VeiculoListDTO":
        return VeiculoListDTO(
            cursor=(
                int(request.query_params.get("cursor"))
                if request.query_params.get("cursor")
                else None
            ),
            limit=int(request.query_params.get("limit", 50)),
            search=request.query_params.get("search"),
            ordering=request.query_params.get("ordering", "-prefixo"),
        )
