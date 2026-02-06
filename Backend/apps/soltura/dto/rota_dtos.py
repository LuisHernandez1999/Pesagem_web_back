from dataclasses import dataclass
from typing import Optional,List


@dataclass
class RotaCreateDTO:
    pa: str
    rota: str
    tipo_servico: str


@dataclass
class RotaUpdateDTO:
    id_rota: int
    pa: str
    rota: str
    tipo_servico: str


@dataclass
class RotaListFiltroDTO:
    pa: Optional[str] = None
    tipo_servico: Optional[str] = None
    cursor: Optional[int] = None
    limit: int = 10

@dataclass
class RotaListResponseDTO:
    items: List["RotaDTO"]
    next_cursor: Optional[int]


@dataclass
class RotaDTO:
    id_rota: int
    pa: str
    rota: str
    tipo_servico: str
