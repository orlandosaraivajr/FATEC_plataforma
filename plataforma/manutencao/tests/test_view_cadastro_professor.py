from django.test import TestCase
from django.shortcuts import resolve_url as r
from core.models import User
from core.facade import CreateTestUser
from manutencao.forms import UserForm


view_in_test = 'manutencao:cadastro_professor'
template_in_test = 'manutencao_index.html'


class editar_empresa_NoAuthGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_templates(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class editar_empresa_Get(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_admin()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_templates(self):
        self.assertEqual(200, self.resp.status_code)


class editar_empresa_Post_Ok(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_admin()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.post(r(view_in_test))
        self.resp2 = self.client.post(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)
