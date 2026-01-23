from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class OrdemServicoCreateDTO:
    pa: str
    os_numero: str
    veiculo_prefixo: str
    inicio_problema: datetime
    conclusao: Optional[datetime] = None
##### RETORONO DO CREATE
@dataclass
class OrdemServicoListDTO:
    id: int
    pa: str
    os_numero: str
    veiculo_id: int
    veiculo_prefixo: str
    inicio_problema: str
    conclusao: Optional[str]
    created_at: str

###### LIST DE DADOS DO DTO, MAS SEM CURSOR 
@dataclass
class OrdemServicoListItemDTO:
    id: int
    pa: str
    os_numero: str
    veiculo_id: int
    veiculo_prefixo: str
    inicio_problema: str
    conclusao: Optional[str]
    created_at: str

#### RESPONSE COMPLETO COM CURSOR
@dataclass
class OrdemServicoListResponseDTO:
    results: list[OrdemServicoListItemDTO]
    next_cursor: Optional[int]
    limit: int

##### DTOS DE FILTROS
@dataclass
class OrdemServicoListFilterDTO:
    cursor_id: Optional[int] = None
    veiculo_prefixo: Optional[str] = None
    os_numero: Optional[str] = None
    pa: Optional[str] = None
    aberta: Optional[bool] = None