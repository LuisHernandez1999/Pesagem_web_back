from django.db import models
from apps.soltura.models.soltura import Soltura
from django.core.exceptions import ValidationError
from django.utils import timezone

class Averiguacao(models.Model):
    tipo_servico = models.CharField(max_length=15, choices=[
        ('Remoção', 'Remoção'),
        ('Seletiva', 'Seletiva'),
        ('Varrição', 'Varrição')
    ], default='Remoção')

    pa_da_averiguacao = models.CharField(max_length=7, choices=[
        ('PA1', 'PA1'), ('PA2', 'PA2'), ('PA3', 'PA3'), ('PA4', 'PA4')
    ], default='PA1')

    data = models.DateField(auto_now_add=True)
    hora_averiguacao = models.TimeField(auto_now_add=True)

    rota_averiguada = models.ForeignKey(
        Soltura,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='averiguacoes_rota'
    )

    imagem1 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem2 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem3 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem4 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem5 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem6 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem7 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)

    averiguador = models.CharField(max_length=15)
    formulario = models.TextField(blank=True, null=True)

    def clean(self):
        super().clean()
        imagens = [
            self.imagem1, self.imagem2, self.imagem3,
            self.imagem4, self.imagem5, self.imagem6, self.imagem7
        ]
        if not any(imagens):
            raise ValidationError("Adicione pelo menos uma imagem à averiguação.")

    class Meta:
        db_table = 'averiguacao'
        managed = True
        indexes = [
            models.Index(fields=['data', 'tipo_servico']),
            models.Index(fields=['averiguador', 'data']),
        ]
