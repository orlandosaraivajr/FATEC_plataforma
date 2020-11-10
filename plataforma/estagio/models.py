from django.utils import timezone
from datetime import timedelta
from django.db import models
from core.facade import User
from core.models import CURSO_FATEC

CATEGORIAS_DOCUMENTO = (
    ('0', 'Termo de compromisso de Estágio'),
    ('1', 'Plano de Atividades'),
    ('2', 'Termo Aditivo'),
    ('3', 'Rescisão de Contrato'),
    ('4', 'Ficha de avaliação do estagiário'),
    ('5', 'Relatório Parcial de Estágio'),
    ('6', 'Relatório Final de Estágio'),
)

VALIDADE_CONVENIO = (
    ('1', '06 meses'),
    ('2', '1 ano'),
    ('3', '2 anos'),
    ('4', '3 anos'),
    ('5', '4 anos'),
    ('6', '5 anos'),
)


class ConvenioModel(models.Model):
    empresa = models.ForeignKey(User, on_delete=models.CASCADE)
    documento = models.FileField(upload_to='convenios_estagio/')
    observacao = models.TextField(default='', blank=True)
    observacao_professor = models.TextField(default='', blank=True)
    aprovado_professor = models.BooleanField(default=False)
    validade = models.CharField(
        verbose_name='Validade Convênio',
        max_length=2,
        choices=VALIDADE_CONVENIO,
        default='6'
    )
    data_validade = models.DateTimeField(
        default=timezone.now() + timedelta(days=1826))
    changed_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def ajuste_data_validade(self):
        if getattr(self, 'validade', True):
            if self.validade == '1':
                self.data_validade = timezone.now() + timedelta(days=180)
            if self.validade == '2':
                self.data_validade = timezone.now() + timedelta(days=365)
            if self.validade == '3':
                self.data_validade = timezone.now() + timedelta(days=731)
            if self.validade == '4':
                self.data_validade = timezone.now() + timedelta(days=1096)
            if self.validade == '5':
                self.data_validade = timezone.now() + timedelta(days=1461)
            if self.validade == '6':
                self.data_validade = timezone.now() + timedelta(days=1826)

    def save(self, *args, **kwargs):
        if getattr(self, 'validade', True):
            self.ajuste_data_validade()
        super(ConvenioModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Convênios de Estágio'
        verbose_name = 'Convênio de Estágio'


class DocumentoEstagioModel(models.Model):
    empresa = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_aluno = models.TextField(default='', blank=False)
    tipo_documento = models.CharField(
        verbose_name='Tipo de Documento',
        max_length=2,
        choices=CATEGORIAS_DOCUMENTO,
        default='1'
    )
    curso_fatec = models.CharField(
        verbose_name='Curso',
        max_length=2,
        choices=CURSO_FATEC,
        default='1'
    )
    documento = models.FileField(upload_to='documentos_estagio/')
    observacao = models.TextField(default='', blank=True)
    observacao_professor = models.TextField(default='', blank=True)
    aprovado_professor = models.BooleanField(default=False)
    changed_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def tipo_de_documento(self):
        return CATEGORIAS_DOCUMENTO[int(self.tipo_documento)][1]

    @property
    def nome_curso(self):
        return CURSO_FATEC[int(self.curso_fatec)][1]

    class Meta:
        verbose_name_plural = 'Documentos de Estágio'
        verbose_name = 'Documento de Estágio'
