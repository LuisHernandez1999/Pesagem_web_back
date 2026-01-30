from django.db import transaction
from django.core.exceptions import ValidationError
from apps.soltura.models.rota import Rota
from apps.soltura.dto.rota_dtos import RotaUpdateDTO, RotaDTO,RotaListFiltroDTO,RotaCreateDTO
from apps.soltura.mappers.rota_mapper import RotaMapper
from apps.soltura.utils.rota_utils import validar_campos_obrigatorios,validar_rota_unica


class CriarRotaService:

    @staticmethod
    @transaction.atomic
    def executar(dto: RotaCreateDTO) -> RotaDTO:

        validar_campos_obrigatorios(dto.garagem, dto.rota, dto.tipo_servico)
        validar_rota_unica( dto.rota, dto.tipo_servico)

        rota = Rota.objects.create(
            pa=dto.garagem,
            rota=dto.rota,
            tipo_servico=dto.tipo_servico,
        )

        return RotaMapper.to_dto(rota)

class AtualizarRotaService:
    @staticmethod
    @transaction.atomic
    def executar(dto: RotaUpdateDTO) -> RotaDTO:
        try:
            rota = Rota.objects.get(id=dto.id_rota)
        except Rota.DoesNotExist:
            raise ValidationError("Rota não encontrada")
        validar_campos_obrigatorios(dto.pa, dto.rota, dto.tipo_servico)
        rota.pa = dto.pa
        rota.rota = dto.rota
        rota.tipo_servico = dto.tipo_servico
        rota.save()

        return RotaMapper.to_dto(rota)



class ListarRotaService:
    @staticmethod
    def executar(dto: RotaListFiltroDTO) -> list[RotaDTO]:
        qs = Rota.objects.all().order_by("pa", "rota")
        if dto.pa:
            qs = qs.filter(pa=dto.pa)
        if dto.tipo_servico:
            qs = qs.filter(tipo_servico=dto.tipo_servico)
        return RotaMapper.to_dto_list(qs)
    

class DeletarRotaService:
    @staticmethod
    @transaction.atomic
    def executar(id_rota: int) -> None:

        try:
            rota = Rota.objects.get(id=id_rota)
        except Rota.DoesNotExist:
            raise ValidationError("Rota não encontrada")

        rota.delete()