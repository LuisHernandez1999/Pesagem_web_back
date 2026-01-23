from django.db import transaction
from django.core.exceptions import ValidationError
from apps.insumos.models import Insumo
from apps.movimentacao.models import Movimentacao
from apps.insumos.dto.insumos_dto import (
    InsumoCreateDTO,
    InsumoListCursorDTO
)


class InsumoServiceCreate:
    @staticmethod
    @transaction.atomic
    def criar(dto: InsumoCreateDTO) -> Insumo:
        # ===== validações =====
        if not dto.item_insumo:
            raise ValidationError("item_insumo é obrigatório")

        try:
            movimentacao = Movimentacao.objects.get(
                id_movimentacao=dto.id_movimentacao
            )
        except Movimentacao.DoesNotExist:
            raise ValidationError("Movimentação não encontrada")

        # ===== criar =====
        return Insumo.objects.create(
            movimentacao=movimentacao,
            item_insumo=dto.item_insumo
        )




class InsumoListService:
    @staticmethod
    def listar_com_cursor(dto: InsumoListCursorDTO):
        qs = Insumo.objects.select_related(
            "movimentacao"
        ).order_by("-id_insumo")

        # ===== filtros =====
        if dto.id_movimentacao:
            qs = qs.filter(
                movimentacao_id=dto.id_movimentacao
            )

        # ===== cursor =====
        if dto.next_cursor:
            qs = qs.filter(
                id_insumo__lt=dto.next_cursor
            )

        # ===== limit + 1 =====
        itens = list(qs[: dto.limit + 1])
        has_next = len(itens) > dto.limit
        itens = itens[: dto.limit]

        next_cursor = (
            itens[-1].id_insumo if has_next and itens else None
        )
        return itens, next_cursor
