from apps.averiguacao.mappers.averiguacao_mapper import AveriguacaoCreateMapper,AveriguacaoEstatisticasSemanaMapper
from apps.averiguacao.dto.averiguacao_dto import(AveriguacaoCreateRequestDTO,AveriguacaoEstatisticasSemanaResponseDTO
                                                 ,MetaSemanaResponseDTO)
from django.db import transaction
from django.db import transaction
from  apps.averiguacao.utils.averiguacao_utils  import validar_campos_obrigatorios


class AveriguacaoServiceCreate:
    @staticmethod
    @transaction.atomic
    def create(dto: AveriguacaoCreateRequestDTO) -> int:
        validar_campos_obrigatorios(dto)
        return AveriguacaoCreateMapper.insert(dto)
    

class AveriguacaoEstatisticasSemanaService:
    def execute(self, dto):
        cards, inicio, fim = (
            AveriguacaoEstatisticasSemanaMapper.map_cards_semana(
                pa=dto.pa,
                turno=dto.turno,
                servico=dto.tipo_servico,
                data_inicio=dto.data_inicio,
                data_fim=dto.data_fim,
            )
        )
        meta_dict = AveriguacaoEstatisticasSemanaMapper.map_meta(
            dto.tipo_servico,
            cards,
        )
        meta = MetaSemanaResponseDTO(**meta_dict)
        return AveriguacaoEstatisticasSemanaResponseDTO(
            periodo_inicio=inicio,
            periodo_fim=fim,
            cards_por_dia=cards,
            meta=meta,
        )

