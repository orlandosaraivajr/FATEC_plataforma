from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import resolve_url as r

from estagio.forms import ConvenioForm
from estagio.models import ConvenioModel
from core.facade import CreateTestUser
from core.facade import User
from plataforma import settings

TINY_GIF = settings.TINY_GIF


class ConvenioFormTest(TestCase):
    def setUp(self):
        self.form = ConvenioForm()

    def test_form_has_fields(self):
        expected = ['empresa', 'documento']
        expected += ['observacao']
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
            'observacao': 'tesTe'
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
