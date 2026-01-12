from django.db import models

class MetaBatida(models.Model):
    meta_toneladas = models.FloatField(default=2601.0)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.meta_toneladas} toneladas (Atualizado em {self.atualizado_em})"
