from dataclasses import  dataclass
from datetime import date,datetime,time
from typing import Dict,Optional


@dataclass
class AveriguacaoCreateRequestDTO:
    tipo_servico: str
    pa_da_averiguacao: str
    rota_averiguada_id: int
    averiguador: str
    formulario: str | None

@dataclass
class AveriguacaoResponseDTO:
    id: int
    tipo_servico: str
    pa_da_averiguacao: str
    data: date
    hora_averiguacao: time
    rota_averiguada_id: int | None
    averiguador: str
    formulario: str | None

@dataclass
class AveriguacaoEstatisticasSemanaRequestDTO:
    tipo_servico: str
    pa: Optional[str] = None
    turno: Optional[str] = None
    data_inicio: Optional[str] = None
    data_fim: Optional[str] = None

@dataclass
class MetaSemanaResponseDTO:
    total: int
    realizado: int
    percentual_realizado: float
    faltante: int
    percentual_faltante: float


@dataclass
class AveriguacaoEstatisticasSemanaResponseDTO:
    periodo_inicio: datetime.date
    periodo_fim: datetime.date
    cards_por_dia: Dict[str, Dict[str, int]]
    meta: MetaSemanaResponseDTO





