from django.db import models

class Rota(models.Model):
    TIPO_SERVICO = [
        ("Seletiva", "Seletiva"),
        ("Domiciliar", "Domiciliar"),
        ("Varrição", "Varrição")
    ]

    PAS=[
        ("PA1", "PA1"),
        ("PA2", "PA2"),
        ("PA3", "PA3"),
        ("PA4", "PA4")
    ]
    
    pa = models.CharField(max_length=10, choices=PAS ,null=False, blank=False)  
    rota = models.CharField(max_length=10, null=False, blank=False)  
    tipo_servico = models.CharField(max_length=10, choices=TIPO_SERVICO, null=False, blank=False)

    class Meta:
        db_table = 'rota'
        unique_together = ['pa', 'rota', 'tipo_servico']  # Garante unicidade por PA, rota e tipo de serviço

    def __str__(self):
        return f"{self.pa} - {self.rota} - {self.tipo_servico}"