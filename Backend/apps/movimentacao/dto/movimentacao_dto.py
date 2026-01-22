from dataclasses import dataclass
from datetime import datetime



@dataclass
class MovimentacaoCreateDTO:
    os_id: int                      # FK → OrdemServico.id
    data_hora: datetime
    status: str
    responsavel_matricula: int      # FK → Colaborador.matricula
    observacao: str 
