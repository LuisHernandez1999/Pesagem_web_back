from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from apps.colaborador.models import Colaborador
from apps.celular.models.celular import Celular
from apps.veiculo.models import Veiculo
from .rota import Rota
from .setor import Setor

class Soltura(models.Model):
    STATUS_CHOICES = [
        ('Em Andamento', 'Em Andamento'),
        ('Concluído', 'Concluído')
    ]

    TIPO_SERVICO = [
        ("Seletiva", "Seletiva"),
        ("Domiciliar", "Domiciliar"),
        ("Remoção", "Remoção"),
        ("Varrição", "Varrição")
    ]

    TURNO_CHOICES = [
        ('Diurno', 'Diurno'),
        ('Noturno', 'Noturno'),
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino')
    ]

    PAS = [
        ("PA1", "PA1"),
        ("PA2", "PA2"),
        ("PA3", "PA3"),
        ("PA4", "PA4")
    ]

    motorista = models.ForeignKey(Colaborador, on_delete=models.CASCADE, limit_choices_to={'funcao__in': ['Motorista', 'Operador'], 'status': 'ATIVO'}, related_name='solturas_motorista')
    coletores = models.ManyToManyField(Colaborador, limit_choices_to={'funcao': 'Coletor', 'status': 'ATIVO'}, related_name='solturas_coletor', blank=True)

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, limit_choices_to={'em_manutencao': 'NÃO'}, related_name='solturas')

    hora_entrega_chave = models.TimeField()
    hora_saida_frota = models.TimeField()
    data_soltura = models.DateField()
    data_criacao = models.DateTimeField(auto_now_add=True, null=True)
    hora_retorno_frota = models.DateTimeField(null=True, blank=True)
    data_referencia = models.DateField(null=True, blank=True)
    
    rota = models.ForeignKey(Rota, on_delete=models.SET_NULL, null=True, blank=True, related_name='solturas')
    garagem = models.CharField(max_length=10, choices=PAS, default='PA1', blank=False, null=False)
    celular = models.CharField(max_length=20, blank=True)
    celular_id = models.ForeignKey(Celular, on_delete=models.SET_NULL, null=True, blank=True, related_name='solturas')#
    lider = models.CharField(max_length=55)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='Em Andamento')
    tipo_servico = models.CharField(max_length=10, choices=TIPO_SERVICO, default='Seletiva')
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, null=True, blank=True, related_name='solturas_setor')


    class Meta:
        db_table = 'soltura'
        

    def __str__(self):
        return f"Soltura - {self.motorista.nome} ({self.veiculo.prefixo if self.veiculo else 'sem veículo'})"

    def clean(self):
        # Verifica se veículo está ativo (caso informado)
        if self.veiculo and self.veiculo.em_manutencao.casefold() != 'não'.casefold():
            raise ValidationError("O veículo associado deve estar ativo.")

        # Validações específicas por tipo de serviço
        if self.tipo_servico == 'Varrição':
            if self.coletores.exists():
                raise ValidationError("Varrição não deve ter coletores.")
            if not self.rota:
                raise ValidationError("Varrição requer uma rota.")
            if self.rota and (self.rota.pa != self.garagem or self.rota.tipo_servico != 'Varrição'):
                raise ValidationError("A rota selecionada não é válida para a garagem ou tipo de serviço Varrição.")

        elif self.tipo_servico == 'Remoção':
            if self.rota:
                raise ValidationError("Remoção não deve ter uma rota.")
            if not self.garagem:
                raise ValidationError("Remoção requer uma garagem.")

            
        elif self.tipo_servico in ['Seletiva', 'Domiciliar']:
            if not self.coletores.exists():
                raise ValidationError(f"{self.tipo_servico} requer pelo menos um coletor.")
            if not self.rota:
                raise ValidationError(f"{self.tipo_servico} requer uma rota.")
            if self.rota and (self.rota.pa != self.garagem or self.rota.tipo_servico != self.tipo_servico):
                raise ValidationError(f"A rota selecionada não é válida para a garagem ou tipo de serviço {self.tipo_servico}.")

        
    def tempo_total_em_servico(self):
        if self.hora_saida_frota and self.hora_retorno_frota:
            saida = self.hora_saida_frota
            retorno = self.hora_retorno_frota.time()
            data_base = datetime(2025, 1, 1)
            saida_dt = datetime.combine(data_base, saida)
            retorno_dt = datetime.combine(data_base, retorno)
            delta = retorno_dt - saida_dt
            if delta.total_seconds() < 0:
                retorno_dt = datetime.combine(data_base + timedelta(days=1), retorno)
                delta = retorno_dt - saida_dt
            horas, resto = divmod(delta.total_seconds(), 3600)
            minutos = resto // 60
            return f"{int(horas)}h {int(minutos)}min"
        return None