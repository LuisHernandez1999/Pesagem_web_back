from dataclasses import  dataclass
from datetime import date,datetime


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







