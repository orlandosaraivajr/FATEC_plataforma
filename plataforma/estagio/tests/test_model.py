from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import resolve_url as r
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from estagio.models import ConvenioModel, DocumentoEstagioModel
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


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class ConvenioModel_validade_convenio_Test(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.client.post(r(self.login_url), data)
        self.empresa = User.objects.all()[0]

    def test_validade_padrao(self):
        convenio = ConvenioModel(
            empresa=self.empresa,
            observacao='',
            documento=SimpleUploadedFile('tiny.pdf', TINY_PDF.read())
        )
        convenio.save()
        data_futura = timezone.now() + timedelta(days=1826)
        self.assertTrue(ConvenioModel.objects.exists())
        self.assertEqual(convenio.data_validade.year, data_futura.year)
        self.assertEqual(convenio.data_validade.month, data_futura.month)
        self.assertEqual(convenio.data_validade.day, data_futura.day)

    def test_validade_06_meses(self):
        convenio = ConvenioModel(
            empresa=self.empresa,
            observacao='nenhuma observação',
            validade='1',
            documento=SimpleUploadedFile('tiny.pdf', TINY_PDF.read())
        )
        convenio.save()
        data_futura = timezone.now() + timedelta(days=180)
        self.assertTrue(ConvenioModel.objects.exists())
        self.assertEqual(convenio.data_validade.year, data_futura.year)
        self.assertEqual(convenio.data_validade.month, data_futura.month)
        self.assertEqual(convenio.data_validade.day, data_futura.day)

    def test_validade_1_ano(self):
        convenio = ConvenioModel(
            empresa=self.empresa,
            observacao='nenhuma observação',
            validade='2',
            documento=SimpleUploadedFile('tiny.pdf', TINY_PDF.read())
        )
        convenio.save()
        data_futura = timezone.now() + timedelta(days=365)
        self.assertTrue(ConvenioModel.objects.exists())
        self.assertEqual(convenio.data_validade.year, data_futura.year)
        self.assertEqual(convenio.data_validade.month, data_futura.month)
        self.assertEqual(convenio.data_validade.day, data_futura.day)

    def test_validade_2_anos(self):
        convenio = ConvenioModel(
            empresa=self.empresa,
            observacao='nenhuma observação',
            validade='3',
            documento=SimpleUploadedFile('tiny.pdf', TINY_PDF.read())
        )
        convenio.save()
        data_futura = timezone.now() + timedelta(days=731)
        self.assertTrue(ConvenioModel.objects.exists())
        self.assertEqual(convenio.data_validade.year, data_futura.year)
        self.assertEqual(convenio.data_validade.month, data_futura.month)
        self.assertEqual(convenio.data_validade.day, data_futura.day)

    def test_validade_3_anos(self):
        convenio = ConvenioModel(
            empresa=self.empresa,
            observacao='nenhuma observação',
            validade='4',
            documento=SimpleUploadedFile('tiny.pdf', TINY_PDF.read())
        )
        convenio.save()
        data_futura = timezone.now() + timedelta(days=1096)
        self.assertTrue(ConvenioModel.objects.exists())
        self.assertEqual(convenio.data_validade.year, data_futura.year)
        self.assertEqual(convenio.data_validade.month, data_futura.month)
        self.assertEqual(convenio.data_validade.day, data_futura.day)

    def test_validade_4_anos(self):
        convenio = ConvenioModel(
            empresa=self.empresa,
            observacao='nenhuma observação',
            validade='5',
            documento=SimpleUploadedFile('tiny.pdf', TINY_PDF.read())
        )
        convenio.save()
        data_futura = timezone.now() + timedelta(days=1461)
        self.assertTrue(ConvenioModel.objects.exists())
        self.assertEqual(convenio.data_validade.year, data_futura.year)
        self.assertEqual(convenio.data_validade.month, data_futura.month)
        self.assertEqual(convenio.data_validade.day, data_futura.day)

    def test_validade_5_anos(self):
        convenio = ConvenioModel(
            empresa=self.empresa,
            observacao='nenhuma observação',
            validade='6',
            documento=SimpleUploadedFile('tiny.pdf', TINY_PDF.read())
        )
        convenio.save()
        data_futura = timezone.now() + timedelta(days=1826)
        self.assertTrue(ConvenioModel.objects.exists())
        self.assertEqual(convenio.data_validade.year, data_futura.year)
        self.assertEqual(convenio.data_validade.month, data_futura.month)
        self.assertEqual(convenio.data_validade.day, data_futura.day)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class DocumentoEstagioModelTest(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.client.post(r(self.login_url), data)
        self.usuario = User.objects.all()[0]
        self.documento = DocumentoEstagioModel(
            empresa=self.usuario,
            observacao='nenhuma observação',
            documento=SimpleUploadedFile('tiny.pdf', TINY_PDF.read())
        )
        self.documento.save()

    def test_create(self):
        self.assertTrue(User.objects.exists())
        self.assertTrue(DocumentoEstagioModel.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.documento.created_at, datetime)

    def test_comentario(self):
        self.assertEqual(self.documento.observacao, 'nenhuma observação')

    def test_comentario_professor(self):
        self.assertEqual(self.documento.observacao_professor, '')

    def test_aprovacao_professor(self):
        self.assertFalse(self.documento.aprovado_professor)

    def test_aluno(self):
        self.assertEqual(self.documento.empresa.id, self.usuario.pk)
