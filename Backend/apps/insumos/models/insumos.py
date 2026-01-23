from django.db import models
from apps.movimentacao.models import Movimentacao


class Insumo(models.Model):
    id_insumo = models.AutoField(
        primary_key=True
    )
    movimentacao = models.ForeignKey(
        Movimentacao,
        on_delete=models.CASCADE,
        db_column="id_movimentacao",
        related_name="insumos"
    )
    item_insumo = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        db_table = "insumos"
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
    def __str__(self):
        return f"{self.item_insumo} (Movimentação {self.movimentacao_id})"
