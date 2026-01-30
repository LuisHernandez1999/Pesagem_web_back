from dataclasses import dataclass
from typing import Optional


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


@dataclass
class RotaDTO:
    id_rota: int
    pa: str
    rota: str
    tipo_servico: str
