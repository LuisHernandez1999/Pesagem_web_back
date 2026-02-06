from dataclasses import  dataclass
from datetime import date,datetime
from typing import Dict,Optional


@dataclass
class AveriguacaoCreateDTO:
    tipo_servico: str 
    pa_da_averiguacao:str
    data:date
    hora_averiguacao:datetime
    rota_da_averiguacao:str
    imagem1:str
    imagem2:str
    imagem3:str
    imagem4:str
    imagem5:str
    imagem6:str
    imagem7:str
    averiguador:str
    formulario:str


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





