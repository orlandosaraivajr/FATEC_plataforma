from django.shortcuts import resolve_url as r
from django.test import TestCase
from core.facade import CreateTestUser
from core.models import User
from vitrine.forms import VitrineForm
from vitrine.models import VitrineModel

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


class vitrine_PostOk(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.resp = self.client.post(r('core:login'), data)
        self.aluno = User.objects.all()[0] 
        data = {
            'aluno': self.aluno.pk, 
            'curso': '0', 
            'tipo_vaga': '2', 
            'descricao': 'quero trabalhar', 
            'linkedin': 'https://www.linkedin.com/in/orlando-saraiva-júnior-83707022/', 
            'github': 'https://github.com/orlandosaraivajr'
            }
        self.resp = self.client.post(r(url_testada), data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'cadastro_feito.html')
        self.assertTemplateUsed(self.resp, 'aluno_sidebar.html')
        self.assertTemplateUsed(self.resp, 'aluno_topbar.html')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_github(self):
        cadastro_feito = VitrineModel.objects.all()[0]
        self.assertEqual(
            cadastro_feito.github, 'https://github.com/orlandosaraivajr')


class vitrine_PostOk2(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.resp = self.client.post(r('core:login'), data)
        self.aluno = User.objects.all()[0] 
        data = {
            'aluno': self.aluno.pk, 
            'curso': '0', 
            'tipo_vaga': '2', 
            'descricao': 'quero trabalhar', 
            'linkedin': '', 
            'github': 'https://github.com/orlandosaraivajr'
            }
        self.resp = self.client.post(r(url_testada), data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'cadastro_feito.html')
        self.assertTemplateUsed(self.resp, 'aluno_sidebar.html')
        self.assertTemplateUsed(self.resp, 'aluno_topbar.html')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_github(self):
        cadastro_feito = VitrineModel.objects.all()[0]
        self.assertEqual(
            cadastro_feito.github, 'https://github.com/orlandosaraivajr')


class vitrine_PostFail(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.resp = self.client.post(r('core:login'), data)
        self.aluno = User.objects.all()[0] 
        data = {
            'aluno': self.aluno.pk, 
            'curso': '0', 
            'tipo_vaga': '2', 
            'descricao': 'quero trabalhar', 
            'linkedin': '', 
            'github': ''
            }
        self.resp = self.client.post(r(url_testada), data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'cadastro.html')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_github(self):
        cadastro_feito = VitrineModel.objects.all()
        self.assertEqual(len(cadastro_feito), 0)


class vitrine_PostFail2(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.resp = self.client.post(r('core:login'), data)
        self.aluno = User.objects.all()[0] 
        data = {
            'aluno': self.aluno.pk, 
            'curso': '0', 
            'tipo_vaga': '2', 
            'descricao': '', 
            'linkedin': 'https://www.linkedin.com/in/orlando-saraiva-júnior-83707022/', 
            'github': 'https://github.com/orlandosaraivajr'
            }
        self.resp = self.client.post(r(url_testada), data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'cadastro.html')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_github(self):
        cadastro_feito = VitrineModel.objects.all()
        self.assertEqual(len(cadastro_feito), 0)