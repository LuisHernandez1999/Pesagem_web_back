from django.db import models

class Setor(models.Model):
    
    nome_setor = models.CharField(max_length=100, null=False, blank=False, unique=True)
    regiao = models.CharField(max_length=100, null=False, blank=False)
    
    class Meta:
        db_table = 'setor'
        indexes = [
            models.Index(fields=['nome_setor']),
            models.Index(fields=['regiao']),
        ]
        
    def __str__(self):
        return f"{self.nome_setor} - {self.regiao}"