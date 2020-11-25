from django.db import models
from django.utils import timezone
from datetime import timedelta
from core.models import CURSO_FATEC, User


TIPO_VAGA = (
    ('0', 'Emprego'),
    ('1', 'Estágio'),
    ('2', 'Emprego ou Estágio'),
)


class VitrineModel(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.TextField()
    linkedin = models.URLField(default='', blank=True)
    github = models.URLField(default='', blank=True)
    curso = models.CharField(
        verbose_name='Curso Matriculado',
        max_length=2,
        choices=CURSO_FATEC,
        default='0'
    )
    tipo_vaga = models.CharField(
        verbose_name='Tipo da Vaga',
        max_length=2,
        choices=TIPO_VAGA,
        default='2'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Alunos cadastrados'
        verbose_name = 'Aluno cadastrado'