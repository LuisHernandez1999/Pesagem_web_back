from dataclasses import dataclass
from datetime import date,time
from typing import Optional, Dict,  List


@dataclass(frozen=True)
class SolturaFiltroDTO:
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None


@dataclass(frozen=True)
class SolturaResumoDTO:
    total_em_andamento: int
    total_concluido: int
    contagem_dia_semana: Dict[int, int]
    contagem_mes: Dict[int, int]
    contagem_dia: Dict[str, int]
    mes_mais_saida: Optional[int]

@dataclass
class SolturaCursorDTO:
    data_soltura: date
    id: int


@dataclass
class SolturaListInputDTO:
    cursor: Optional[SolturaCursorDTO] = None
    page_size: int = 20
    filters: Optional[Dict] = None
    search: Optional[Dict] = None
    q: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


@dataclass
class SolturaListItemDTO:
    id: int
    motorista: str | None
    coletores: list
    garagem: str
    data_soltura: date
    setor: str | None
    turno: str
    status: str
    prefixo: str | None


@dataclass
class SolturaListOutputDTO:
    items: List[SolturaListItemDTO]
    next_cursor: Optional[SolturaCursorDTO]




@dataclass
class SolturaCreateDTO:
    motorista_id: int
    coletores_ids: List[int]
    veiculo_id: int
    hora_entrega_chave: time
    hora_saida_frota: time
    data_soltura: date
    garagem: str
    lider: str
    tipo_servico: str
    turno: str
    rota_id: Optional[int] = None
    setor_id: Optional[int] = None
    celular_id: Optional[int] = None
    celular: Optional[str] = None


@dataclass
class SolturaCreateResponseDTO:
    id: int
    status: str
    tipo_servico: str
    data_soltura: date