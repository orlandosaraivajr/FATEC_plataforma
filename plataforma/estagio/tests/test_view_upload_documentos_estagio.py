from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.shortcuts import resolve_url as r
from core.facade import User
from core.facade import CreateTestUser
from estagio.models import DocumentoEstagioModel
from estagio.forms import DocumentoEstagioForm
from plataforma import settings

TINY_GIF = settings.TINY_GIF
view_in_test = 'estagio:upload_documentos_estagio'
template_in_test = 'upload_documentos_estagio.html'


class uploadDocumentosEstagioNoAuthGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_template_home(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class uploadDocumentosEstagioGet(TestCase, CreateTestUser):
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
            ('<form', 2),
            ('<input', 6),
            ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, DocumentoEstagioForm)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class uploadDocumentosEstagioPostOk(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))
        self.imagem_mock = SimpleUploadedFile('tiny.gif', TINY_GIF)
        self.data = {}
        self.data['empresa'] = User.objects.all()[0].pk
        self.data['observacao'] = "agendado próxima visita"
        self.data['nome_aluno'] = "Estagiário"
        self.data['tipo_documento'] = "1"
        self.data['curso_fatec'] = "1"
        self.data['documento'] = self.imagem_mock
        self.resp = self.client.post(r(view_in_test), self.data)

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_data(self):
        self.assertTrue(DocumentoEstagioModel.objects.exists())

    def test_template(self):
        self.assertTemplateUsed(self.resp, "arquivo_enviado_com_sucesso.html")

@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class uploadDocumentosEstagioPostNoFile(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))

        self.data = {}
        self.data['empresa'] = User.objects.all()[0].pk
        self.data['observacao'] = "comentário"

        self.resp = self.client.post(r(view_in_test), self.data)

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_not_saved_data(self):
        self.assertFalse(DocumentoEstagioModel.objects.exists())

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)
