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
