from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.shortcuts import resolve_url as r
from core.functions import register_new_company
from core.models import User
from core.facade import CreateTestUser
from estagio.models import ConvenioModel
from estagio.forms import ProfessorConvenioForm
from plataforma import settings

TINY_GIF = settings.TINY_GIF
view_in_test = 'estagio:professor_upload_convenio'
template_in_test = 'professor_upload_convenio.html'


class uploadProfessorConvenioEstagioNoAuthGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_template_home(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class uploadProfessorConvenioEstagioGetOk(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_template_home(self):
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, ProfessorConvenioForm)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class uploadProfConvenioEstagioGet_access_denied(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test), follow=True)
        self.resp2 = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'index.html')
        self.assertTemplateUsed(self.resp, 'rodape.html')

    def test_200_300_statuscode(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(302, self.resp2.status_code)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class uploadProfessorConvenioEstagioPostOk(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))
        self.imagem_mock = SimpleUploadedFile('tiny.gif', TINY_GIF)
        register_new_company('empresa@empresa.com', '123')
        register_new_company('empresa2@empresa.com', '123')
        self.data = {}
        self.data['empresa'] = User.objects.all()[1].pk
        self.data['observacao'] = "agendado próxima visita"
        self.data['validade'] = "1"
        self.data['documento'] = self.imagem_mock
        self.resp = self.client.post(r(view_in_test), self.data)

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_data(self):
        self.assertTrue(ConvenioModel.objects.exists())

    def test_template(self):
        self.assertTemplateUsed(self.resp, "arquivo_enviado_com_sucesso.html")


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class uploadProfConvenioEstagioPost_access_denied(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))
        self.imagem_mock = SimpleUploadedFile('tiny.gif', TINY_GIF)
        self.data = {}
        self.data['empresa'] = User.objects.all()[0].pk
        self.data['observacao'] = "agendado próxima visita"
        self.data['validade'] = "1"
        self.data['documento'] = self.imagem_mock
        self.resp = self.client.post(r(view_in_test), self.data)

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_data(self):
        self.assertFalse(ConvenioModel.objects.exists())

    def test_template(self):
        self.assertTemplateUsed(self.resp, "professor_upload_convenio.html")
        self.assertTemplateUsed(self.resp, "professor_sidebar.html")


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class uploadConvenioEstagioPostNoFile(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))

        self.data = {}
        self.data['empresa'] = User.objects.all()[0].pk
        self.data['observacao'] = "comentário"

        self.resp = self.client.post(r(view_in_test), self.data)

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_not_saved_data(self):
        self.assertFalse(ConvenioModel.objects.exists())

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)
