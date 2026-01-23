from dataclasses import dataclass
from datetime import datetime,date
from typing import Optional

####REQUEST E REPONSE SAI NESSE PADRÃO
@dataclass
class MovimentacaoCreateDTO:
    os_numero: str                  
    data_hora: datetime
    status: str
    responsavel_matricula: int      # FK → Colaborador.matricula
    observacao: str 



@dataclass
class MovimentacaoListCursorDTO:
    pa: Optional[str] = None
    data: Optional[date] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    os_id: Optional[int] = None
    os_numero: Optional[str] = None
    status: Optional[str] = None
    responsavel_matricula: Optional[int] = None
    responsavel_nome: Optional[str] = None
    veiculo_prefixo: Optional[str] = None
    observacao: Optional[str] = None
    next_cursor: int = None
    limit: int = 20


@dataclass
class MovimentacaoListDTO:
    id: int
    os_id: int
    os_numero: str
    pa: str
    veiculo_prefixo: str
    data_hora: str
    status: str
    responsavel_matricula: int
    responsavel_nome: str
    observacao: Optional[str]