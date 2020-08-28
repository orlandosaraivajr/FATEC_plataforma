from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import resolve_url as r

from estagio.forms import ConvenioForm, DocumentoEstagioForm
from estagio.models import ConvenioModel, DocumentoEstagioModel
from core.facade import CreateTestUser
from core.facade import User
from plataforma import settings

TINY_GIF = settings.TINY_GIF


class ConvenioFormTest(TestCase):
    def setUp(self):
        self.form = ConvenioForm()

    def test_form_has_fields(self):
        expected = ['empresa', 'documento']
        expected += ['validade', 'observacao']
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_renomear_arquivo(self):
        novo_nome = self.form.renomear_arquivo('arquivo.pdf')
        self.assertEqual(len(novo_nome), 69)
        self.assertTrue(novo_nome.endswith('.pdf'))
        novo_nome = self.form.renomear_arquivo('arquivo.jpeg')
        self.assertEqual(len(novo_nome), 69)
        self.assertTrue(novo_nome.endswith('.jpeg'))


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class DataConvenioFormTest(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.client.post(r(self.login_url), data)
        empresa = User.objects.all()[0]
        data = {
            'empresa': empresa.pk,
            'observacao': 'tesTe',
            'validade': '1'
        }
        file_data = {
            'documento': SimpleUploadedFile('file.gif', TINY_GIF)
        }
        self.form = ConvenioForm(data, file_data)
        self.validated = self.form.is_valid()
        self.form.save()

    def test_valid_form(self):
        self.assertTrue(self.validated)

    def test_create(self):
        self.assertTrue(ConvenioModel.objects.exists())

    def test_observacao_upper(self):
        self.assertEqual('TESTE', self.form.cleaned_data['observacao'])

    def test_validade(self):
        self.assertEqual('1', self.form.cleaned_data['validade'])


class DocumentoEstagioTest(TestCase):
    def setUp(self):
        self.form = DocumentoEstagioForm()

    def test_form_has_fields(self):
        expected = ['empresa', 'tipo_documento']
        expected += ['curso_fatec', 'nome_aluno']
        expected += ['documento', 'observacao']
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_renomear_arquivo(self):
        novo_nome = self.form.renomear_arquivo('arquivo.pdf')
        self.assertEqual(len(novo_nome), 69)
        self.assertTrue(novo_nome.endswith('.pdf'))
        novo_nome = self.form.renomear_arquivo('arquivo.jpeg')
        self.assertEqual(len(novo_nome), 69)
        self.assertTrue(novo_nome.endswith('.jpeg'))


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class DataDocumentoEstagioFormTest(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.client.post(r(self.login_url), data)
        empresa = User.objects.all()[0]
        data = {
            'empresa': empresa.pk,
            'curso_fatec': 0,
            'tipo_documento': 0,
            'nome_aluno': 'José da Silva',
            'observacao': 'tesTe'
        }
        file_data = {
            'documento': SimpleUploadedFile('file.gif', TINY_GIF)
        }
        self.form = DocumentoEstagioForm(data, file_data)
        self.validated = self.form.is_valid()
        self.form.save()

    def test_valid_form(self):
        self.assertTrue(self.validated)

    def test_create(self):
        self.assertTrue(DocumentoEstagioModel.objects.exists())

    def test_observacao_upper(self):
        self.assertEqual('TESTE', self.form.cleaned_data['observacao'])

    def test_nome_aluno_upper(self):
        self.assertEqual('JOSÉ DA SILVA', self.form.cleaned_data['nome_aluno'])
