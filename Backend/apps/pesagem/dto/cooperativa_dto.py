from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCooperativaDTO:
    nome: str

    def __post_init__(self):
        if not self.nome or not self.nome.strip():
            raise ValueError("Nome da cooperativa é obrigatório")
