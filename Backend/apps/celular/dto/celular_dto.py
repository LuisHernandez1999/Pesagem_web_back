from dataclasses import dataclass
from datetime import date



@dataclass
class CelularCreateDTO:
    numero:str
    ativo:bool
    modelo:str
    fabricante:str
    garagem_atual: str
    codigo_imei:str
    apelido:str

@dataclass
class CelularCreateResponseDTO:
    id: int
    numero:str
    ativo:bool
    modelo:str
    fabricante:str
    garagem_atual: str
    codigo_imei:str
    apelido:str




