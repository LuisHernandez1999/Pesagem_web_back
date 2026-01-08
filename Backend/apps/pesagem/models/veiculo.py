from django.db import models

class Veiculo(models.Model):
    TIPOS_VEICULO = [
        ('Basculante', 'Basculante'),
        ('Selectolix', 'Selectolix'),
        ('Baú', 'Baú'),
        ('Pá Carregadeira', 'Pá Carregadeira'),
        ('Retroescavadeira', 'Retroescavadeira'),
        ('Compactador', 'Compactador'),
        ('Varredeira', 'Varredeira'),
        
    ]

    TIPOS_SERVICO = [
        ('Seletiva', 'Seletiva'),
        ('Domiciliar', 'Domiciliar'),
        ('Remoção', 'Remoção'),
        ('Varrição', 'Varrição'),
    ]
    prefixo = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_VEICULO)
    placa_veiculo = models.CharField(max_length=8, blank=True, null=True, unique=True, verbose_name="Placa do Veículo")  
    em_manutencao = models.CharField(
        max_length=3,
        choices=[('SIM', 'Sim'), ('NÃO', 'Não')],
        default='NÃO',
        verbose_name="Em Manutenção"
    )
    tipo_servico = models.CharField(
        max_length=11,
        choices=TIPOS_SERVICO,
        default='Seletiva',
        verbose_name="Tipo de Serviço"
    )
    equipamento = models.CharField(max_length=3, choices=[('Sim', 'Sim'), ('Não', 'Não')], default='Não',null=False, blank=False, verbose_name="Equipamento")

    class Meta:
        db_table = 'veiculo'
        
    def __str__(self):
        return f"{self.prefixo} - {self.tipo}"
