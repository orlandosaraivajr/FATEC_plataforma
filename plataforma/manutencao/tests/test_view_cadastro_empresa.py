from django.test import TestCase
from django.shortcuts import resolve_url as r
from core.models import User
from core.facade import CreateTestUser
from manutencao.forms import UserForm


view_in_test = 'manutencao:cadastro_empresa'
template_in_test = 'cadastro_empresa.html'


class cadastro_empresa_NoAuthGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_templates(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class cadastro_empresa_Get(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_admin()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_templates(self):
        self.assertEqual(200, self.resp.status_code)

    def test_context(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, UserForm)

    def test_html(self):
        tags = (
            ('<div', 38),
            ('</div>', 38),
            ('<input', 5),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class cadastro_empresa_Post_Ok(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_admin()
        self.resp = self.client.post(r('core:login'), data)
        data = dict(email='orlando@saraiva.com', password='1234mud@r')
        self.resp = self.client.post(r(view_in_test), data)
        self.resp2 = self.client.post(r(view_in_test), data, follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, template_in_test)

    def test_user_created(self):
        gravado = len(User.objects.filter(email__exact='orlando@saraiva.com'))
        self.assertEquals(1, gravado)

    def test_user_created_email(self):
        usuario = User.objects.filter(email__exact='orlando@saraiva.com')[0]
        self.assertEquals(usuario.email, 'orlando@saraiva.com')
        self.assertEquals(usuario.username, 'orlando@saraiva.com')

    def test_user_created_password(self):
        usuario = User.objects.filter(email__exact='orlando@saraiva.com')[0]
        self.assertNotEquals(usuario.password, '1234mud@r')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class cadastro_empresa_Post_Fail(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_admin()
        self.resp = self.client.post(r('core:login'), data)
        data = dict(email='orlando@saraiva.com')
        self.resp = self.client.post(r(view_in_test), data)
        self.resp2 = self.client.post(r(view_in_test), data, follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)

    def test_user_created(self):
        gravado = len(User.objects.filter(email__exact='orlando@saraiva.com'))
        self.assertEquals(0, gravado)
