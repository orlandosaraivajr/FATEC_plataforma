from django.test import TestCase, override_settings
from django.shortcuts import resolve_url as r
from core.models import User
from core.facade import CreateTestUser
from plataforma import settings

TINY_GIF = settings.TINY_GIF
view_in_test = 'estagio:listar_relatorio_parcial_estagio'
template_in_test = 'listar_documentos.html'


class ListarRelatorioParcialEstagioNoAuthGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_template_home(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class ListarRelatorioParcialEstagioGetOk(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_template_home(self):
        self.assertEqual(200, self.resp.status_code)

    def test_html(self):
        tags = (
            ('Termo de compromisso', 1),
            ('Plano de Atividades', 1),
            ('Termo Aditivo', 0),
            ('Rescisão de Contrato', 1),
            ('Ficha de avaliação', 1),
            ('Relatório Parcial', 2),
            ('Relatório Final', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)