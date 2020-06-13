from django.shortcuts import resolve_url as r
from django.test import TestCase
from core.functions import (register_new_student, register_new_teacher,
                            register_new_company)


class coreGetIndex(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:home'))
        self.resp2 = self.client.get(r('core:home'), follow=True)

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetLoginOk(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:login'))

    def test_302_response(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'login.html')


class corePostLoginOK(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        register_new_student(self.username, self.password)
        data = {
            'username': self.username,
            'password': self.password
        }
        self.resp = self.client.post(r('core:login'), data)
        self.resp2 = self.client.post(r('core:login'), data, follow=True)

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'index.html')


class corePostLoginFail(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        data = {
            'username': self.username,
            'password': self.password
        }
        self.resp = self.client.post(r('core:login'), data)
        self.resp2 = self.client.post(r('core:login'), data, follow=True)

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'login.html')


class coreGetIndexAlunoFail(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:core_index_aluno'))
        self.resp2 = self.client.get(r('core:core_index_aluno'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexAlunoOk(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        register_new_student(self.username, self.password)
        data = {
            'username': self.username,
            'password': self.password, }
        self.client.post(r('core:login'), data)
        self.resp = self.client.get(r('core:core_index_aluno'))
        self.resp2 = self.client.get(r('core:core_index_aluno'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'aluno_index.html')

    def test_200_response_1(self):
        self.assertEqual(200, self.resp.status_code)

    def test_200_response_2(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexProfessorFail(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:core_index_professor'))
        self.resp2 = self.client.get(
            r('core:core_index_professor'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexProfessorOk(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        register_new_teacher(self.username, self.password)
        data = {'username': self.username, 'password': self.password}
        self.client.post(r('core:login'), data)
        self.resp = self.client.get(r('core:core_index_professor'))
        self.resp2 = self.client.get(
            r('core:core_index_professor'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'professor_index.html')

    def test_200_response_1(self):
        self.assertEqual(200, self.resp.status_code)

    def test_200_response_2(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexEmpresaFail(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:core_index_empresa'))
        self.resp2 = self.client.get(
            r('core:core_index_empresa'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_302_response(self):
        self.assertEqual(302, self.resp.status_code)

    def test_200_response(self):
        self.assertEqual(200, self.resp2.status_code)


class coreGetIndexEmpresaOk(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        register_new_company(self.username, self.password)
        data = {'username': self.username, 'password': self.password}
        self.client.post(r('core:login'), data)
        self.resp = self.client.get(r('core:core_index_empresa'))
        self.resp2 = self.client.get(
            r('core:core_index_empresa'), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'empresa_index.html')

    def test_200_response_1(self):
        self.assertEqual(200, self.resp.status_code)

    def test_200_response_2(self):
        self.assertEqual(200, self.resp2.status_code)
