from dataclasses import dataclass
from typing import Optional, List


# ==================================================
# CREATE
# ==================================================

@dataclass
class CelularCreateDTO:
    numero: str
    ativo: bool
    modelo: str
    fabricante: str
    garagem_atual: str
    codigo_imei: str
    apelido: str


@dataclass
class CelularCreateResponseDTO:
    id: int
    numero: str
    ativo: bool
    modelo: str
    fabricante: str
    garagem_atual: str
    codigo_imei: str
    apelido: str


# ==================================================
# LIST (SCROLL INFINITO)
# ==================================================

@dataclass
class CelularListRequestDTO:
    cursor: int = 0


@dataclass
class CelularListDTO:
    numero: str
    ativo: bool
    modelo: str
    fabricante: str
    garagem_atual: str
    codigo_imei: str
    apelido: str


@dataclass
class CelularListResponseDTO:
    results: List[CelularListDTO]
    next_cursor: Optional[int]
    has_next: bool
    limit: int = 10


# ==================================================
# DELETE
# ==================================================

@dataclass
class CelularDeleteRequestDTO:
    celular_id: int


@dataclass
class CelularDeleteResponseDTO:
    message: str


# ==================================================
# UPDATE (PATCH)
# ==================================================

@dataclass
class CelularUpdateRequestDTO:
    celular_id: int
    numero: Optional[str] = None
    ativo: Optional[bool] = None
    modelo: Optional[str] = None
    fabricante: Optional[str] = None
    garagem_atual: Optional[str] = None
    codigo_imei: Optional[str] = None
    apelido: Optional[str] = None


@dataclass
class CelularUpdateResponseDTO:
    id: int
    numero: str
    ativo: bool
    modelo: str
    fabricante: str
    garagem_atual: str
    codigo_imei: str
    apelido: str
