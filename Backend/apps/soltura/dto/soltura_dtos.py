from dataclasses import dataclass
from datetime import date,time
from typing import Optional, Dict,List, TypeVar,Generic

T = TypeVar("T")



@dataclass
class SolturaCreateDTO:
    tipo_servico: str
    garagem: str
    rota_id: int
    data_soltura: date
    turno: str
    hora_entrega_chave: time
    hora_saida_frota: time
    veiculo_id: int
    motorista_id: int
    coletores_ids: List[int]
    status: Optional[str] = "Em Andamento"

@dataclass
class SolturaFiltroDTO:
    search: Optional[str] = None
    status: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    column_filters: Dict[str, str] | None = None
    limit: int = 10


@dataclass
class CursorDTO:
    id: int
    data_soltura: str


@dataclass
class SolturaListItemDTO:
    id: int
    motorista: Optional[str]
    coletores: List[str]
    garagem: str
    data_soltura: date
    rota: Optional[str]
    setor: Optional[str]
    turno: str
    status: str
    prefixo: Optional[str]


@dataclass
class ListResponseDTO(Generic[T]):
    items: List[T]
    total: int
    next_cursor: Optional[dict]


@dataclass
class SolturaListInputDTO:
    tipo_servico: str
    filtro: SolturaFiltroDTO
    cursor: Optional[CursorDTO] = None



##### dtofiltros pragraficos 

@dataclass
class SolturaAnalyticsFiltroDTO:
    tipo_servico: str
    filtro_fn: callable  # <--- agora é obrigatório no DTO
    status: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None