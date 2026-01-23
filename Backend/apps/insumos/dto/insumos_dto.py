from dataclasses import dataclass
from typing import Optional


@dataclass
class InsumoCreateDTO:
    id_movimentacao: int
    item_insumo: str


@dataclass
class InsumoListCursorDTO:
    id_movimentacao: Optional[int] = None
    next_cursor: Optional[int] = None
    limit: int = 20
