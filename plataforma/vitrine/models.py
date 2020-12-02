from datetime import timedelta
from django.db import models
from django.db.models import Q
from django.utils import timezone
from core.models import CURSO_FATEC, User


TIPO_VAGA = (
    ('0', 'Emprego'),
    ('1', 'Estágio'),
    ('2', 'Emprego ou Estágio'),
)


class VitrineManager(models.Manager):
    def get_alunos(self):
        one_month_ago = timezone.now() - timedelta(days=30)
        return VitrineModel.objects.filter(
            updated_at__gte=one_month_ago
        ).order_by('updated_at')
    
    def get_alunos_emprego(self):
        alunos = self.get_alunos()
        return alunos.filter(Q(tipo_vaga=0) | Q(tipo_vaga=2))

    def get_alunos_estagio(self):
        alunos = self.get_alunos()
        return alunos.filter(Q(tipo_vaga=1) | Q(tipo_vaga=2))

    def get_tipo_vaga(self, tipo_vaga):
        alunos = self.get_alunos()
        return alunos.filter(Q(tipo_vaga=tipo_vaga) | Q(tipo_vaga=2))
    
    def get_tipo_curso(self, curso):
        alunos = self.get_alunos()
        return alunos.filter(curso=curso)


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
    objects = VitrineManager()

    class Meta:
        verbose_name_plural = 'Alunos cadastrados'
        verbose_name = 'Aluno cadastrado'
    
    def __str__(self):
        return f'{self.aluno.first_name} - {self.aluno.email}'
