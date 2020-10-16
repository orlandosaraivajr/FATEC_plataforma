
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.shortcuts import resolve_url as r
from core.models import User
from core.facade import CreateTestUser
from estagio.models import ConvenioModel
from plataforma import settings

TINY_GIF = settings.TINY_GIF
view_in_test = 'estagio:listar_todos_convenios'
template_in_test = 'listar_convenios.html'


class listar_todos_convenios_NoAuthGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_template_home(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class listar_todos_convenios_Get(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test), follow=True)
        self.resp2 = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)

class listar_todos_convenios_Fail_access_denied(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test), follow=True)
        self.resp2 = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(302, self.resp2.status_code)


class listar_todos_convenios_Post(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test), follow=True)
        self.resp2 = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)