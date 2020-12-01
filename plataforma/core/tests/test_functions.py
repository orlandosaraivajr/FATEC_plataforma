from django.contrib.auth import get_user_model
from django.test import TestCase

from core.functions import (register_new_teacher, register_new_company,
                            register_new_student, register_new_admin,
                            authenticate, update_user, register_student)
from core.models import User


class register_fails(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.student = register_new_student(self.username, None)
        self.teacher = register_new_teacher(self.username, None)
        self.company = register_new_company(self.username, None)
        self.admin = register_new_admin(self.username, None)

    def test_failed_create_users(self):
        self.assertFalse(self.student)
        self.assertFalse(self.teacher)
        self.assertFalse(self.company)
        self.assertFalse(self.admin)


class register_OK(TestCase):
    def setUp(self):
        self.password = '123mudar'
        self.student = register_new_student('student@teste.br', self.password)
        self.teacher = register_new_teacher('teacher@teste.br', self.password)
        self.company = register_new_company('company@teste.br', self.password)
        self.admin = register_new_admin('admin@fatec.sp.gov.br', self.password)

    def test_ok_create_users(self):
        self.assertTrue(self.student)
        self.assertTrue(self.teacher)
        self.assertTrue(self.company)
        self.assertTrue(self.admin)


class Register_new_company_Test(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        User = get_user_model()
        register_new_company(self.username, self.password)
        self.user = User.objects.get(email=self.username)

    def test_created(self):
        self.assertTrue(User.objects.exists())

    def test_email(self):
        self.assertEqual(self.user.email, self.username)

    def test_password(self):
        self.assertNotEqual(self.user.password, self.password)

    def test_username(self):
        self.assertEqual(self.user.username, self.username)

    def test_is_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_is_teacher(self):
        self.assertFalse(self.user.is_teacher)

    def test_is_company(self):
        self.assertTrue(self.user.is_company)

    def test_is_student(self):
        self.assertFalse(self.user.is_student)


class Register_new_teacher_Test(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        User = get_user_model()
        register_new_teacher(self.username, self.password)
        self.user = User.objects.get(email=self.username)

    def test_created(self):
        self.assertTrue(User.objects.exists())

    def test_email(self):
        self.assertEqual(self.user.email, self.username)

    def test_password(self):
        self.assertNotEqual(self.user.password, self.password)

    def test_username(self):
        self.assertEqual(self.user.username, self.username)

    def test_is_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_is_teacher(self):
        self.assertTrue(self.user.is_teacher)

    def test_is_company(self):
        self.assertFalse(self.user.is_company)

    def test_is_student(self):
        self.assertFalse(self.user.is_student)


class Register_new_student_Test(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        User = get_user_model()
        register_new_student(self.username, self.password)
        self.user = User.objects.get(email=self.username)

    def test_created(self):
        self.assertTrue(User.objects.exists())

    def test_email(self):
        self.assertEqual(self.user.email, self.username)

    def test_password(self):
        self.assertNotEqual(self.user.password, self.password)

    def test_username(self):
        self.assertEqual(self.user.username, self.username)

    def test_is_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_is_teacher(self):
        self.assertFalse(self.user.is_teacher)

    def test_is_company(self):
        self.assertFalse(self.user.is_company)

    def test_is_student(self):
        self.assertTrue(self.user.is_student)


class Register_new_admin_Test(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        User = get_user_model()
        register_new_admin(self.username, self.password)
        self.user = User.objects.get(email=self.username)

    def test_created(self):
        self.assertTrue(User.objects.exists())

    def test_email(self):
        self.assertEqual(self.user.email, self.username)

    def test_password(self):
        self.assertNotEqual(self.user.password, self.password)

    def test_username(self):
        self.assertEqual(self.user.username, self.username)

    def test_is_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_is_teacher(self):
        self.assertFalse(self.user.is_teacher)

    def test_is_company(self):
        self.assertFalse(self.user.is_company)

    def test_is_student(self):
        self.assertFalse(self.user.is_student)

    def test_is_superuser(self):
        self.assertTrue(self.user.is_superuser)


class Authenticate_OK_Test(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        register_new_student(self.username, self.password)
        self.user = authenticate(self.username, self.password)

    def test_email(self):
        self.assertEqual(self.user.username, self.username)

    def test_password(self):
        self.assertNotEqual(self.user.password, self.password)

    def test_username(self):
        self.assertEqual(self.user.username, self.username)

    def test_is_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_is_teacher(self):
        self.assertFalse(self.user.is_teacher)

    def test_is_company(self):
        self.assertFalse(self.user.is_company)

    def test_is_student(self):
        self.assertTrue(self.user.is_student)


class Authenticate_Fail_no_user_Test(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        self.user = authenticate(self.username, self.password)

    def test_no_user_returned(self):
        self.assertEqual(self.user, None)


class Authenticate_Fail_user_not_active_Test(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.password = '123mudar'
        User = get_user_model()
        register_new_student(self.username, self.password)
        change_user = User.objects.get(email=self.username)
        change_user.is_active = False
        change_user.save()
        self.user = authenticate(self.username, self.password)

    def test_no_user_returned(self):
        self.assertEqual(self.user, None)


class Update_user_test_1(TestCase):
    def setUp(self):
        self.username = 'user@user.br'
        self.old_password = '123mudar'
        self.new_password = '321mudar'
        User = get_user_model()
        register_new_student(self.username, self.old_password)
        id = User.objects.get(email='user@user.br').pk
        self.returned = update_user(id, self.new_password)
        self.user = authenticate(self.username, self.new_password)

    def test_updated_ok(self):
        self.assertTrue(self.returned)

    def test_email(self):
        self.assertEqual(self.user.username, self.username)

    def test_first_name(self):
        self.assertEqual(self.user.first_name, '')

    def test_last_name(self):
        self.assertEqual(self.user.last_name, '')


class Update_user_test_2(TestCase):
    def setUp(self):
        self.username = 'user@user.br'
        self.old_password = '123mudar'
        self.new_password = '321mudar'
        User = get_user_model()
        register_new_student(self.username, self.old_password)
        id = User.objects.get(email='user@user.br').pk
        self.returned = update_user(id, self.new_password,'John','Doe')
        self.user = authenticate(self.username, self.new_password)

    def test_updated_ok(self):
        self.assertTrue(self.returned)

    def test_email(self):
        self.assertEqual(self.user.username, self.username)

    def test_first_name(self):
        self.assertEqual(self.user.first_name, 'John')

    def test_last_name(self):
        self.assertEqual(self.user.last_name, 'Doe')


class Update_user_test_3(TestCase):
    def setUp(self):
        self.username = 'user@user.br'
        self.old_password = '123mudar'
        User = get_user_model()
        register_new_student(self.username, self.old_password)
        id = User.objects.get(email='user@user.br').pk
        self.returned = update_user(id)
        self.user = authenticate(self.username, self.old_password)

    def test_updated_fail(self):
        self.assertFalse(self.returned)

    def test_email(self):
        self.assertEqual(self.user.username, self.username)

    def test_first_name(self):
        self.assertEqual(self.user.first_name, '')

    def test_last_name(self):
        self.assertEqual(self.user.last_name, '')


class register_student_kwargs_OK(TestCase):
    def setUp(self):
        context = dict(first_name='Orlando', last_name='Saraiva',
                       username='aluno_teste@fatec.sp.gov.br',
                       password='123mud@r')
        self.register = register_student(**context)

    def test_saved(self):
        self.assertTrue(self.register)


class register_student_kwargs_Fail(TestCase):
    def setUp(self):
        context = dict(first_name='Orlando', last_name='Saraiva',
                       password='123mud@r')
        self.register = register_student(**context)

    def test_saved(self):
        self.assertFalse(self.register)