from django.db import models
from django.utils.timezone import now
from .veiculo import Veiculo
from .cooperativa import Cooperativa
from .colaborador import Colaborador

class Pesagem(models.Model):
    VOLUMES_CARGA = {
        'Basculante': {'Alto': 300, 'Médio': 150, 'Baixo': 75},
        'Selectolix': {'Alto': 2050, 'Médio': 1025, 'Baixo': 512.5},
        'Baú': {'Alto': 2250, 'Médio': 1125, 'Baixo': 562.5},
    } 
    TIPOS_PESAGEM = (
        ('SELETIVA', 'Seletiva'),
        ('CATA-TRECO', 'Cata-treco'),
    )
    GARAGENS = (
        ('PA1', 'PA1'),
        ('PA2', 'PA2'),
        ('PA3', 'PA3'),
        ('PA4', 'PA4'),
        ('SEM GARAGEM', 'Sem Garagem'),
    )

    data = models.DateField(default=now)
    prefixo_id = models.ForeignKey(Veiculo, on_delete=models.CASCADE, db_column='prefixo_id')
    colaborador_id = models.ManyToManyField('Colaborador', related_name='pesagens_coletores')
    cooperativa_id = models.ForeignKey(Cooperativa, on_delete=models.CASCADE, db_column='cooperativa_id')
    responsavel_coop = models.CharField(max_length=100, blank = True, null=True)
    motorista_id = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='pesagens_motorista', db_column='motorista_id')
    hora_chegada = models.TimeField()
    hora_saida = models.TimeField()
    numero_doc = models.CharField(max_length=9, unique=True)
    volume_carga = models.CharField(max_length=10)
    tipo_pesagem = models.CharField(max_length=20, choices=TIPOS_PESAGEM, default='SELETIVA')
    peso_calculado = models.DecimalField(max_digits=10, decimal_places=3, default=0, editable=False)
    garagem = models.CharField(max_length=12, choices=GARAGENS, default='SEM GARAGEM')
    turno = models.CharField(max_length=10, choices=(('Diurno', 'Diurno'), ('Noturno', 'Noturno'), ('SEM TURNO', 'SEM TURNO')), default='SEM TURNO') 
    class Meta:
        indexes = [            
            models.Index(fields=['data']),
            models.Index(fields=['numero_doc']),
            models.Index(fields=['prefixo_id']),
            models.Index(fields=['motorista_id']),
            models.Index(fields=['cooperativa_id']),
            models.Index(fields=['volume_carga']),
            models.Index(fields=['peso_calculado']),
            models.Index(fields=['hora_chegada']),
            models.Index(fields=['hora_saida']),
            models.Index(fields=['responsavel_coop']),
            models.Index(fields=['garagem']),
            models.Index(fields=['turno']),
            models.Index(fields=['tipo_pesagem']),
            
        ]
        
        db_table = 'pesagem'
        
    def calcular_peso(self):
        """Calcula o peso automaticamente baseado no volume e tipo do veículo."""
        
        if not self.prefixo_id or not self.volume_carga:
            return 0
        try:            
            tipo_veiculo = self.prefixo_id.tipo
            volume_carga = self.volume_carga
        except AttributeError:
            return 0
        
        return self.VOLUMES_CARGA.get(tipo_veiculo, {}).get(volume_carga, 0)
    
        
    def save(self, *args, **kwargs):
        self.peso_calculado = self.calcular_peso()
        super().save(*args, **kwargs)    
    
    def __str__(self):
        return f"Pesagem de {self.prefixo_id} - {self.data} - {self.peso_calculado}kg"
    