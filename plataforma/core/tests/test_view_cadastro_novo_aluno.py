from django.test import TestCase
from django.shortcuts import resolve_url as r
from core.models import User
from core.facade import CreateTestUser
from plataforma import settings

TINY_GIF = settings.TINY_GIF
view_in_test = 'core:cadastro_novo_aluno'
template_in_test = 'cadastro_novo_aluno.html'


class cadastro_novo_aluno_Get(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_create(self):
        self.assertFalse(User.objects.exists())

    def test_template(self):
        self.assertTemplateUsed(self.resp2, template_in_test)

    def test_200_template_home(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)

    def test_html(self):
        tags = (
            ('<form', 1),
            ('<input', 5),
            ('<input type="hidden"', 1),
            ('<input type="text"', 2),
            ('<input type="email"', 1),
            ('<input type="password"', 1),
            ('<button type="submit"', 1),
            ('</form>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class cadastro_novo_aluno_PostOk(TestCase):
    def setUp(self):
        self.data = dict(first_name='Orlando', last_name='Saraiva', 
                         username='orlando.nascimento@fatec.sp.gov.br',
                         password='123mud@r')
        self.resp = self.client.post(r(view_in_test), self.data)
        self.resp2 = self.client.post(r(view_in_test),
                                      self.data, follow=True)

    def test_create(self):
        self.assertTrue(User.objects.exists())

    def test_200(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class cadastro_novo_aluno_PostFail(TestCase):
    def setUp(self):
        self.data = dict(first_name='Orlando', last_name='Saraiva', 
                         username='',
                         password='123mud@r')
        self.resp = self.client.post(r(view_in_test), self.data)
        self.resp2 = self.client.post(r(view_in_test),
                                      self.data, follow=True)

    def test_create(self):
        self.assertFalse(User.objects.exists())
        self.assertEquals(len(User.objects.all()), 0)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)

    def test_html(self):
        tags = (
            ('<form', 1),
            ('<input', 5),
            ('<input type="hidden"', 1),
            ('<input type="text"', 2),
            ('<input type="email"', 1),
            ('<input type="password"', 1),
            ('<button type="submit"', 1),
            ('</form>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class cadastro_novo_aluno_PostFail2(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.cadastro = User(
            username='orlando.nascimento@fatec.sp.gov.br',
            email='orlando.nascimento@fatec.sp.gov.br',
            password='123mudar', first_name='Orlando',
            last_name='Saraiva Jr')
        self.cadastro.save()
        self.data = dict(first_name='Orlando', last_name='Saraiva', 
                         username='orlando.nascimento@fatec.sp.gov.br',
                         password='123mud@r')
        self.resp = self.client.post(r(view_in_test), self.data)
        self.resp2 = self.client.post(r(view_in_test),
                                      self.data, follow=True)

    def test_create(self):
        self.assertTrue(User.objects.exists())
        self.assertEquals(len(User.objects.all()), 1)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)

    def test_html(self):
        tags = (
            ('<form', 1),
            ('<input', 5),
            ('<input type="hidden"', 1),
            ('<input type="text"', 2),
            ('<input type="email"', 1),
            ('<input type="password"', 1),
            ('<button type="submit"', 1),
            ('</form>', 1),
            ('Um usuário com este nome de usuário já existe.', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)