from django.test import TestCase
from django.shortcuts import resolve_url as r
from core.facade import CreateTestUser
from django.contrib.auth import get_user_model
from core.functions import register_new_teacher, update_user


view_in_test = 'manutencao:editar_usuario'
template_in_test = 'editar_usuarios.html'


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
        register_new_teacher('user@user.br', '123mudar')
        User = get_user_model()
        data = {}
        data['user_id'] = User.objects.get(email='user@user.br').pk
        data['password'] = '321mudar'
        data['first_name'] = 'John'
        data['last_name'] = 'Doe'
        self.resp = self.client.post(r(view_in_test), data, follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'cadastro_edicao_concluido.html')
        self.assertTemplateUsed(self.resp, 'manutencao_sidebar.html')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_user_changed(self):
        User = get_user_model()
        user = User.objects.get(email='user@user.br')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')


class editar_empresa_Post_Ok2(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_admin()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.post(r(view_in_test))
        register_new_teacher('user@user.br', '123mudar')
        User = get_user_model()
        self.id = User.objects.get(email='user@user.br').pk
        update_user(self.id, '1234mudar', 'José', 'Silva')
        data = {}
        data['user_id'] = self.id
        data['password'] = '321mudar'
        data['first_name'] = 'John'
        data['last_name'] = 'Doe'
        self.resp = self.client.post(r(view_in_test), data, follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'cadastro_edicao_concluido.html')
        self.assertTemplateUsed(self.resp, 'manutencao_sidebar.html')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_user_changed(self):
        User = get_user_model()
        user = User.objects.get(pk=self.id)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
    
    def test_user(self):
        User = get_user_model()
        user = User.objects.get(pk=self.id)
        self.assertEqual(str(user), 'John Doe')


class editar_empresa_Post_Fail_1(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_admin()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.post(r(view_in_test))
        register_new_teacher('user@user.br', '123mudar')
        User = get_user_model()
        self.id = User.objects.get(email='user@user.br').pk
        data = {}
        data['user_id'] = self.id
        data['password'] = ''
        self.resp = self.client.post(r(view_in_test), data, follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_user_changed(self):
        User = get_user_model()
        user = User.objects.get(pk=self.id)
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
    
    def test_user(self):
        User = get_user_model()
        user = User.objects.get(pk=self.id)
        self.assertEqual(str(user), 'user@user.br')


class editar_empresa_Post_Fail_2(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_admin()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.post(r(view_in_test))
        register_new_teacher('user@user.br', '123mudar')
        User = get_user_model()
        self.id = User.objects.get(email='user@user.br').pk
        data = {}
        data['user_id'] = ''
        data['password'] = '321mudar'
        data['first_name'] = 'John'
        data['last_name'] = 'Doe'
        self.resp = self.client.post(r(view_in_test), data, follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_user_changed(self):
        User = get_user_model()
        user = User.objects.get(pk=self.id)
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
    
    def test_user(self):
        User = get_user_model()
        user = User.objects.get(pk=self.id)
        self.assertEqual(str(user), 'user@user.br')