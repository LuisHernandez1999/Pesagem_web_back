from dataclasses import dataclass
from typing import Optional, Dict,List,Any

@dataclass(slots=True)
class AveriguacaoCreateRequestDTO:
    rota_id: int
    tipo_servico: str
    pa_da_averiguacao: str
    averiguador: Optional[str] = None
    formulario: Optional[str] = None
    imagem1: Optional[str] = None
    imagem2: Optional[str] = None
    imagem3: Optional[str] = None
    imagem4: Optional[str] = None
    imagem5: Optional[str] = None
    imagem6: Optional[str] = None
    imagem7: Optional[str] = None

@dataclass
class AveriguacaoCreateResponseDTO:
    id: int
    mensagem: str

@dataclass(slots=True)
class AveriguacaoEstatisticasSemanaResponseDTO:
    periodo_inicio: str
    periodo_fim: str
    cards_por_dia: Dict[str, Dict[str, int]]
    meta: Dict[str, float]

    def to_dict(self) -> dict:
        return {
            "periodo_inicio": self.periodo_inicio,
            "periodo_fim": self.periodo_fim,
            "cards_por_dia": self.cards_por_dia,
            "meta": self.meta,
        }



@dataclass
class AveriguacaoItemDTO:
    id: int
    data: str
    averiguador: str
    pa_da_averiguacao: str
    tipo_servico: str
    formulario: dict
    soltura_id: Optional[int]
    rota_id: Optional[int]
    rota: str
    nao_conformes: int
    inadequados: int
    detalhes_nao_conformes: List[str]
    detalhes_inadequados: List[str]

@dataclass
class AveriguacaoListResponseDTO:
    items: List[AveriguacaoItemDTO]
    total_count: int



@dataclass
class MotoristaDTO:
    nome: str
    matricula: str

@dataclass
class ColetorDTO:
    nome: str
    matricula: str

@dataclass
class AveriguacaoDTO:
    id: int
    formulario: Dict[str, Any]
    imagens: List[str]
    motorista: Optional[MotoristaDTO]
    coletores: List[ColetorDTO]
    prefixo_veiculo: Optional[str]

@dataclass
class AveriguacaoResponseDTO:
    success: bool
    data: List[AveriguacaoDTO]
    message: Optional[str] = None
    error: Optional[str] = None



@dataclass
class VistoriaDTO:
    vistoria_id: int
    rota_nome: str
    pa: str
    taxas: Dict[str, Dict]

@dataclass
class LiderDTO:
    averiguador: str
    total_averiguacoes: int
    pas: List[str]
    rotas_setores: List[str]
    tipos_servico: List[str]
    turnos: List[str]
    dias_semana: List[str]

@dataclass
class ReportAveriguacaoDTO:
    periodo: str
    pa: Optional[str]
    turno: Optional[str]
    servico: str
    dias_semana: List[str]
    total_respostas: int
    conformidade_servico: Dict
    total_nao_conformes: int
    vistorias: List[VistoriaDTO]
    lideres: List[LiderDTO]
    next_cursor: Optional[int]
    previous_cursor: Optional[int]