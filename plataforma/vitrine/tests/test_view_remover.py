from django.shortcuts import resolve_url as r
from django.test import TestCase
from core.facade import CreateTestUser
from core.models import User
from vitrine.forms import VitrineForm
from vitrine.models import VitrineModel

url_testada = 'vitrine:remover'


class VitrineRemoverNoAuth(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(url_testada))
        self.resp2 = self.client.get(r(url_testada), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'login.html')
        self.assertTemplateUsed(self.resp2, 'base.html')

    def test_200_or_302_responses(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class VitrineRemoverGet_sem_anuncio(TestCase, CreateTestUser):
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


class VitrineRemoverGet_com_anuncio(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.resp = self.client.post(r('core:login'), data)
        self.aluno = User.objects.all()[0]
        data = {'aluno': self.aluno, 'curso': '0', 'tipo_vaga': '2',
                'descricao': 'quero trabalhar', 'linkedin': '',
                'github': 'https://github.com/orlandosaraivajr'}
        VitrineModel.objects.create(**data)
        self.resp = self.client.get(r(url_testada))

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'remover.html')

    def test_200_templates(self):
        self.assertEqual(200, self.resp.status_code)


class VitrineRemoverPOST(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.resp = self.client.post(r('core:login'), data)
        self.aluno = User.objects.all()[0]
        data = {'aluno': self.aluno, 'curso': '0', 'tipo_vaga': '2',
                'descricao': 'quero trabalhar', 'linkedin': '',
                'github': 'https://github.com/orlandosaraivajr'}
        VitrineModel.objects.create(**data)
        self.resp = self.client.post(r(url_testada))

    def test_removed(self):
        cadastro = VitrineModel.objects.filter(aluno_id=self.aluno.pk)
        self.assertEquals(len(cadastro), 0)
        
    def test_template(self):
        self.assertTemplateUsed(self.resp, 'cadastro_feito.html')

    def test_200_templates(self):
        self.assertEqual(200, self.resp.status_code)