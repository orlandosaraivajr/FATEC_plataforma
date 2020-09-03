from django.shortcuts import resolve_url as r
from django.test import TestCase
from core.tests.test_view import CreateTestUser

url_testada = 'core:core_index_manutencao'


class coreGetIndexAdminOk(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_admin()
        self.client.post(r(self.login_url), data)
        self.resp = self.client.get(r(url_testada))
        self.resp2 = self.client.get(r(url_testada), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'rodape.html')
        self.assertTemplateUsed(self.resp2, 'manutencao_sidebar.html')
        self.assertTemplateUsed(self.resp2, 'manutencao_topbar.html')
        self.assertTemplateUsed(self.resp2, 'manutencao_index.html')

    def test_200_or_302_responses(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexAdmin_Fail_NoLogin(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(url_testada))
        self.resp2 = self.client.get(r(url_testada), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_or_302_responses(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexAdmin_Fail_StudentLogin(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.client.post(r(self.login_url), data)
        self.resp = self.client.get(r(url_testada))
        self.resp2 = self.client.get(
            r(url_testada), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'index.html')

    def test_200_or_302_responses(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexAdmin_Fail_ProfessorLogin(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.client.post(r(self.login_url), data)
        self.resp = self.client.get(r(url_testada))
        self.resp2 = self.client.get(
            r(url_testada), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'index.html')

    def test_200_or_302_responses(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexAdmin_Fail_EmpresaLogin(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.client.post(r(self.login_url), data)
        self.resp = self.client.get(r(url_testada))
        self.resp2 = self.client.get(r(url_testada), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'base.html')
        self.assertTemplateUsed(self.resp2, 'index.html')

    def test_200_or_302_responses(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)
