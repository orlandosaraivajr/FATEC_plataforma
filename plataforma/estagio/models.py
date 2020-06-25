from django.db import models
from core.facade import User


class ConvenioModel(models.Model):
    empresa = models.ForeignKey(User, on_delete=models.CASCADE)
    documento = models.FileField(upload_to='convenios_estagio/')
    observacao = models.TextField(default='', blank=True)
    observacao_professor = models.TextField(default='', blank=True)
    aprovado_professor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Convênios de Estágio'
        verbose_name = 'Convênio de Estágio'
