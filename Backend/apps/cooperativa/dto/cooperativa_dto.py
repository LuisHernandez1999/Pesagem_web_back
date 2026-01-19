from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateCooperativaDTO:
    nome: str
    def __post_init__(self):
        if not self.nome or not self.nome.strip():
            raise ValueError("Nome da cooperativa é obrigatório")




@dataclass(frozen=True, slots=True)
class CooperativaEficienciaDTO:
    nome: Optional[str] = None

        