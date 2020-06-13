from django.contrib.auth import get_user_model
from django.test import TestCase

from core.functions import (register_new_teacher, register_new_company,
                            register_new_student, authenticate)
from core.models import User


class register_fails(TestCase):
    def setUp(self):
        self.username = 'orlando.nascimento@fatec.sp.gov.br'
        self.student = register_new_student(self.username, None)
        self.teacher = register_new_teacher(self.username, None)
        self.company = register_new_company(self.username, None)

    def test_failed_create_users(self):
        self.assertFalse(self.student)
        self.assertFalse(self.teacher)
        self.assertFalse(self.company)


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
