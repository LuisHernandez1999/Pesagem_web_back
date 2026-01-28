from django.db import models


class ConfirmacaoServico(models.Model):
    TIPO_SERVICO = [
        ("Remoção", "Remoção"),
        ("Seletiva", "Seletiva"),
        ("Domiciliar", "Domiciliar"),
    ]
    tag_doc = models.CharField(max_length=14, db_index=True, unique=True)#### endcoder 64 gera
    nome_vistoriador = models.CharField(max_length=20, db_index=True, default="USER")
    data_servico = models.DateField(db_index=True)##### preenchido pelo datepiker no frontend 
    tipo_servico = models.CharField(max_length=15, choices=TIPO_SERVICO, db_index=True)### user seleciona 
    class Meta:
        db_table = 'confirmacao_servico'
    def __str__(self):
        return f"{self.tag_doc} - {self.tipo_servico}"
    

class ImagemConfirmacao(models.Model):
    confirmacao = models.ForeignKey(
        ConfirmacaoServico,
        related_name="imagens",
        on_delete=models.CASCADE,
        db_index=True
    )
    imagem = models.URLField(max_length=600)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True) 
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Imagem {self.id} - {self.confirmacao.tag_doc}"
