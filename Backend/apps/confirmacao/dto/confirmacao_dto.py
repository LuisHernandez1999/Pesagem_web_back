from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class ImagemConfirmacaoCreateDTO:
    imagem: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class ConfirmacaoServicoCreateDTO:
    nome_vistoriador: str
    data_servico: date
    tipo_servico: str
    imagens: List[ImagemConfirmacaoCreateDTO]


@dataclass
class ConfirmacaoServicoDTO:
    id: int
    tag_doc: str
    nome_vistoriador: str
    data_servico: date
    tipo_servico: str
    imagens: list
