from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.shortcuts import resolve_url as r
from core.models import User
from core.facade import CreateTestUser
from estagio.models import DocumentoEstagioModel
from plataforma import settings

TINY_GIF = settings.TINY_GIF
view_in_test = 'estagio:validar_documento_estagio'
template_in_test = 'validar_documento_estagio.html'


class validar_documento_estagio_NoAuthGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_template_home(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class validar_documento_estagio_Get(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'professor_index.html')

    def test_200_or_302(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class validar_documento_estagio_Post(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        self.documento = DocumentoEstagioModel(
            empresa=User.objects.all()[0],
            nome_aluno='José da Silva',
            curso_fatec=0,
            tipo_documento=0,
            observacao='nenhuma observação',
            documento=SimpleUploadedFile('tiny.pdf', TINY_GIF)
        )
        self.documento.save()
        data = {'documento_id': self.documento.pk}
        self.resp = self.client.post(r(view_in_test), data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_html(self):
        tags = (
            ('Módulo Empresa', 0),
            ('Módulo Professor', 1),
            ('<div', 41),
            ('</div>', 41),
            ('/media/', 1),
            ('<input', 6),
            ('.pdf', 1),
            ('Aprovar Documentação de Estágio', 1),
            ('José da Silva', 1),
            ('Termo de compromisso de Estágio', 1),
            ('Sistemas para Internet', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class validar_documento_estagio_NoDataPost(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        data = {}
        self.resp = self.client.post(r(view_in_test), data)
        self.resp2 = self.client.post(r(view_in_test), data, follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'professor_index.html')

    def test_200_or_302(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)
