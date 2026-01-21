from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrdemServicoCreateDTO:
    pa: str
    os_numero: str
    veiculo_id: int
    inicio_problema: datetime
