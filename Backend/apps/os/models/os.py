from django.db import models
from apps.veiculo.models import Veiculo


class OrdemServico(models.Model):
    pa = models.CharField(
        max_length=20,
        verbose_name="Posto de Apoio (PA)"
    )

    os_numero = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número da OS"
    )

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name='ordens_servico',
        db_column='prefixo_id',
        verbose_name="Veículo"
    )

    inicio_problema = models.DateTimeField(
        verbose_name="Início do Problema"
    )

    conclusao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Conclusão"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        db_table = 'os'
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        indexes = [
            models.Index(fields=['veiculo'], name='fk_os_veiculo'),
        ]

    def __str__(self):
        return f"OS {self.os_numero} - {self.veiculo.prefixo}"
