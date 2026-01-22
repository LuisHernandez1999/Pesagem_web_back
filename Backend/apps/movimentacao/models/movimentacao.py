from django.db import models
from apps.os.models import OrdemServico
from apps.colaborador.models import Colaborador


class Movimentacao(models.Model):
    id_movimentacao = models.AutoField(
        primary_key=True
    )

    os = models.ForeignKey(
        OrdemServico,
        on_delete=models.PROTECT,
        db_column='id_os',
        related_name='movimentacoes'
    )

    data_hora = models.DateTimeField(
        verbose_name="Data e Hora da Movimentação"
    )

    status = models.CharField(
        max_length=30,
        verbose_name="Status"
    )
    responsavel = models.ForeignKey(
        Colaborador,
        to_field='matricula',              #  FK NA MATRÍCULA
        db_column='responsavel_matricula',
        on_delete=models.PROTECT,
        related_name='movimentacoes'
    )
    observacao = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observação"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'movimentacao'
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'
        indexes = [
            models.Index(fields=['os'], name='fk_mov_os'),
            models.Index(fields=['responsavel'], name='fk_mov_colaborador'),
            models.Index(fields=['status']),
            models.Index(fields=['data_hora']),
        ]

    def __str__(self):
        return f"Movimentação OS {self.os.os_numero} - {self.status}"
