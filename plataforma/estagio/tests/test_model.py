from datetime import datetime
from django.shortcuts import resolve_url as r
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from estagio.models import ConvenioModel
from core.facade import CreateTestUser
from core.facade import User
from plataforma import settings

TINY_PDF = settings.TINY_PDF


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class ConvenioModelTest(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.client.post(r(self.login_url), data)
        self.empresa = User.objects.all()[0]
        self.convenio = ConvenioModel(
            empresa=self.empresa,
            observacao='nenhuma observação',
            documento=SimpleUploadedFile('tiny.pdf', TINY_PDF.read())
        )
        self.convenio.save()

    def test_create(self):
        self.assertTrue(User.objects.exists())
        self.assertTrue(ConvenioModel.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.convenio.created_at, datetime)

    def test_comentario(self):
        self.assertEqual(self.convenio.observacao, 'nenhuma observação')

    def test_comentario_professor(self):
        self.assertEqual(self.convenio.observacao_professor, '')

    def test_aprovacao_professor(self):
        self.assertFalse(self.convenio.aprovado_professor)

    def test_empresa(self):
        self.assertEqual(self.convenio.empresa.id, self.empresa.pk)
