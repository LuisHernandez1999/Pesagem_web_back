from dataclasses import dataclass
from rest_framework.request import Request
from typing import List, Optional

@dataclass(frozen=True)
class CreatePesagemDTO:
    data: str
    prefixo: str                    
    colaboradores: List[str]         
    cooperativa: str                 
    responsavel_coop: Optional[str]
    motorista: str   
    peso_calculado: str                  
    hora_chegada: str
    hora_saida: str
    numero_doc: str
    volume_carga: str                
    tipo_pesagem: str                
    garagem: str                     
    turno: str 


@dataclass
class PesagemListDTO:
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    prefixo: Optional[str] = None
    motorista: Optional[str] = None
    volume_carga: Optional[str] = None
    cooperativa: Optional[str] = None
    numero_doc: Optional[str] = None
    responsavel_coop: Optional[str] = None
    tipo_pesagem: Optional[str] = None
    garagem: Optional[str] = None
    turno: Optional[str] = None
    limit: int = 20
    cursor_id: int = None



@dataclass
class ExibirPesagemPorMesDTO:
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    tipo_pesagem: Optional[str] = None