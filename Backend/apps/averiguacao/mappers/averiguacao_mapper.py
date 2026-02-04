from apps.averiguacao.models.averiguacao import Averiguacao
from apps.averiguacao.dto.averiguacao_dto import AveriguacaoCreateDTO

class AveriguacaoCreateMapper:
    @staticmethod
    def insert(dto:AveriguacaoCreateDTO)->Averiguacao :
         averiguacao= Averiguacao.objects.create(
            tipo_servico=dto.tipo_servico,
            pa_da_averiguacao=dto.pa_da_averiguacao,
            data=dto.data,
            hora_averiguacao=dto.hora_da_averiguacao,
            rota_da_averiguacao=dto.rota_da_averiguacao,
            imagem1=dto.imagem1,
            imagem2=dto.imagem2,
            imagem3=dto.imagem3,
            imagem4=dto.imagem4,
            imagem5=dto.imagem5,
            imagem6=dto.imagem6,
            imagem7=dto.imagem7,
        )
         return averiguacao.id
    




 
 
        