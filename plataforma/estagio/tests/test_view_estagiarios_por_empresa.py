from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.shortcuts import resolve_url as r
from core.models import User
from core.facade import CreateTestUser
from estagio.models import DocumentoEstagioModel
from plataforma import settings

TINY_GIF = settings.TINY_GIF
view_in_test = 'estagio:estagiarios_por_empresa'
template_in_test = 'estagiarios_por_empresa.html'


class convenio_por_empresa_NoAuthGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_template_home(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class convenio_por_empresa_Get(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.resp = self.client.post(r('core:login'), data)
        self.empresa = User.objects.all()[0]
        self.convenio = DocumentoEstagioModel(
            empresa=self.empresa,
            tipo_documento=1,
            nome_aluno='Orlando',
            observacao='nenhuma observação',
            documento=SimpleUploadedFile('tiny.pdf', TINY_GIF)
        )
        self.convenio.save()
        self.resp = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_template_home(self):
        self.assertEqual(200, self.resp.status_code)

    def test_html(self):
        tags = (
            ('Módulo Empresa', 1),
            ('Módulo Professor', 0),
            ('<div', 36),
            ('</div>', 36),
            ('/media/', 1),
            ('<input', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class convenio_por_empresa_NoDataGet(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_template_home(self):
        self.assertEqual(200, self.resp.status_code)

    def test_html(self):
        tags = (
            ('Módulo Empresa', 1),
            ('Módulo Professor', 0),
            ('<div', 29),
            ('</div>', 29),
            ('/media/', 0),
            ('<input', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class convenio_por_empresa_Post(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.post(r(view_in_test))
        self.resp2 = self.client.post(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'empresa_index.html')

    def test_200_or_302(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)
