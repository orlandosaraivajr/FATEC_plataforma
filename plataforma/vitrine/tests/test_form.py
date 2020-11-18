from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import resolve_url as r


from core.functions import register_new_company
from core.facade import CreateTestUser
from core.facade import User
from plataforma import settings

from vitrine.forms import VitrineForm
from vitrine.models import VitrineModel

TINY_GIF = settings.TINY_GIF


class VitrineFormTest(TestCase):
    def setUp(self):
        self.form = VitrineForm()

    def test_form_has_fields(self):
        expected = ['aluno','descricao', 'linkedin']
        expected += ['github', 'curso', 'tipo_vaga']
        self.assertSequenceEqual(expected, list(self.form.fields))

class DataVitrineFormTest(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.client.post(r(self.login_url), data)
        aluno = User.objects.all()[0]
        data = {
            'aluno': aluno.pk,
            'descricao': 'tesTe',
            'linkedin': 'www.linkedin.com/orlandosaraivajr',
            'github': 'www.github.com/orlandosaraivajr',
            'curso' : '0',
            'tipo_vaga': '2'
        }

        self.form = VitrineForm(data)
        self.validated = self.form.is_valid()
        self.form.save()
    
    def test_valid_form(self):
        self.assertTrue(self.validated)

    def test_create(self):
        self.assertTrue(VitrineModel.objects.exists())
    
    def test_descricao(self):
        self.assertEqual('tesTe', self.form.cleaned_data['descricao'])

    def test_curso(self):
        self.assertEqual('0', self.form.cleaned_data['curso'])

    def test_github(self):
        self.assertEqual('http://www.github.com/orlandosaraivajr', self.form.cleaned_data['github'])

    def test_linkedin(self):
        self.assertEqual('http://www.linkedin.com/orlandosaraivajr', self.form.cleaned_data['linkedin'])

    def test_curso(self):
        self.assertEqual('0', self.form.cleaned_data['curso'])

    def test_tipo_vaga(self):
        self.assertEqual('2', self.form.cleaned_data['tipo_vaga'])


class WrongDataVitrineForm(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.client.post(r(self.login_url), data)
        aluno = User.objects.all()[0]
        data = {
            'aluno': aluno.pk,
            'descricao': '',
            'linkedin': '',
            'github': 'www.github.com/orlandosaraivajr',
            'curso' : '0',
            'tipo_vaga': '2'
        }

        self.form = VitrineForm(data)
        self.validated = self.form.is_valid()

    
    def test_valid_form(self):
        self.assertFalse(self.validated)
    
    def test_erro_descricao(self):
        mensagemEsperada = "Você precisa nos contar algo sobre você."
        self.assertEqual(self.form.errors['descricao'][0], mensagemEsperada)

    def test_erro_linkedin(self):
        mensagemEsperada = "Linkedin não pode ser vazio."
        self.assertEqual(self.form.errors['linkedin'][0], mensagemEsperada)