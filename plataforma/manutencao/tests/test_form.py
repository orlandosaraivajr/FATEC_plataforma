from django.test import TestCase, override_settings
from manutencao.forms import UserCreateForm, UserEditForm
from core.models import User
from core.functions import register_new_teacher


class UserCreateFormTest(TestCase):
    def setUp(self):
        self.form = UserCreateForm()

    def test_form_has_fields(self):
        expected = ['email', 'password']
        self.assertSequenceEqual(expected, list(self.form.fields))


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class UserCreateFormTest_Data(TestCase):
    def setUp(self):
        self.form = self.make_validated_form()
        self.validated = self.form.is_valid()
        self.form.save()

    def test_valid_form(self):
        self.assertTrue(self.validated)

    def test_create(self):
        self.assertTrue(User.objects.exists())

    def test_email_malformed(self):
        form = self.make_validated_form(email='xyx')
        self.assertTrue(form.errors)
        msg = '* Insira um endereço de email válido.'
        self.assertEquals(form.errors['email'].as_text(), msg)

    def test_password_not_optional(self):
        form = self.make_validated_form(password='')
        self.assertTrue(form.errors)
        msg = '* Informe a senha provisória.'
        self.assertEquals(form.errors['password'].as_text(), msg)

    def test_password_less_than_8_chars(self):
        form = self.make_validated_form(password='123abc')
        self.assertTrue(form.errors)
        msg = '* A senha precisa ter pelo menos 8 caracteres.'
        self.assertEquals(form.errors['password'].as_text(), msg)

    def test_password_one_number_char(self):
        form = self.make_validated_form(password='abcdefghi')
        self.assertTrue(form.errors)
        msg = '* A senha precisa ter pelo menos um número.'
        self.assertEquals(form.errors['password'].as_text(), msg)

    def test_email_not_optional(self):
        form = self.make_validated_form(email='')
        self.assertTrue(form.errors)
        msg = '* Informe o e-mail. Não deixe este campo em branco'
        self.assertEquals(form.errors['email'].as_text(), msg)

    def test_email_in_use(self):
        form = self.make_validated_form()
        self.assertTrue(form.errors)
        msg = '* Este e-mail está em uso. Digite outro e-mail.'
        self.assertEquals(form.errors['email'].as_text(), msg)

    def make_validated_form(self, **kwargs):
        valid = dict(email='orlando@saraiva.com', password='1234mud@r')
        data = dict(valid, **kwargs)
        form = UserCreateForm(data)
        form.is_valid()
        return form


class UserEditFormTest(TestCase):
    def setUp(self):
        self.form = UserEditForm()

    def test_form_has_fields(self):
        expected = ['first_name', 'last_name', 'password','user_id']
        self.assertSequenceEqual(expected, list(self.form.fields))


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class UserEditFormTest_Data(TestCase):
    def setUp(self):
        register_new_teacher('orlando@saraiva.com', '123mudar')
        self.form = self.make_validated_form()
        self.validated = self.form.is_valid()
        self.form.save()

    def test_valid_form(self):
        self.assertTrue(self.validated)

    def test_create(self):
        self.assertTrue(User.objects.exists())

    def test_password_not_optional(self):
        form = self.make_validated_form(password='')
        self.assertTrue(form.errors)
        msg = '* Informe a nova senha.'
        self.assertEquals(form.errors['password'].as_text(), msg)

    def test_password_less_than_8_chars(self):
        form = self.make_validated_form(password='123abc')
        self.assertTrue(form.errors)
        msg = '* A senha precisa ter pelo menos 8 caracteres.'
        self.assertEquals(form.errors['password'].as_text(), msg)

    def test_password_one_number_char(self):
        form = self.make_validated_form(password='abcdefghi')
        self.assertTrue(form.errors)
        msg = '* A senha precisa ter pelo menos um número.'
        self.assertEquals(form.errors['password'].as_text(), msg)

    def make_validated_form(self, **kwargs):
        user = User.objects.all()[0]
        valid = dict(user_id=user.pk, password='1234mud@r',
                      first_name='Orlando', last_name='1234mud@r')
        data = dict(valid, **kwargs)
        form = UserEditForm(data)
        form.is_valid()
        return form
