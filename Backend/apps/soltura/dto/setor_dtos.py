from dataclasses import dataclass
from typing import Optional

@dataclass
class SetorCreateDTO:
    nome_setor: str
    regiao: str

@dataclass
class SetorResponseDTO:
    id: int
    nome_setor: str
    regiao: str
