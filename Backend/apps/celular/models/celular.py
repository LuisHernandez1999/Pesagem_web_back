from django.db import models
class Celular(models.Model):
    GARAGEM_CHOICES = [
    ('PA1', 'PA1'),
    ('PA2', 'PA2'),
    ('PA3', 'PA3'),
    ('PA4', 'PA4'),
]
    numero = models.CharField(max_length=15, unique=True, null=False, blank=False)
    ativo = models.BooleanField(default=True, null=False, blank=False)
    modelo = models.CharField(max_length=100, null=True, blank=True)
    fabricante = models.CharField(max_length=50, null=True, blank=True)
    garagem_atual = models.CharField(max_length=4, choices=GARAGEM_CHOICES, null=False, blank=False)
    codigo_imei = models.CharField(max_length=20, unique=True, null=True, blank=True)
    apelido = models.CharField(max_length=15, unique=True ,null=False, blank=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'celular'
        indexes = [
            models.Index(fields=['data_criacao']),
            models.Index(fields=['garagem_atual']),
        ]
        
    def __str__(self):
        return f"{self.apelido} - {self.numero}"