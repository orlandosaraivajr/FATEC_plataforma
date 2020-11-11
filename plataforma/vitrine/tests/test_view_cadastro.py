from django.shortcuts import resolve_url as r
from django.test import TestCase
from core.facade import CreateTestUser
from vitrine.forms import VitrineForm

url_testada = 'vitrine:cadastro'


class vitrineGetWithoutAuth(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(url_testada))
        self.resp2 = self.client.get(r(url_testada), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'login.html')
        self.assertTemplateUsed(self.resp2, 'base.html')

    def test_200_or_302_responses(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)

class vitrineGetWithAuth(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(url_testada))

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'cadastro.html')

    def test_200_templates(self):
        self.assertEqual(200, self.resp.status_code)

    def test_context(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, VitrineForm)