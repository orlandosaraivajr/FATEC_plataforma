from django.test import TestCase
from core.forms import CadastroNovoAlunoForm
from core.models import User


class CadastroNovoAlunoFormTest(TestCase):
    def setUp(self):
        self.form = CadastroNovoAlunoForm()

    def test_form_has_fields(self):
        expected = ['first_name', 'last_name', 'username', 'password']
        self.assertSequenceEqual(expected, list(self.form.fields))


class CadastroNovoAlunoFormTest_Data(TestCase):
    def setUp(self):
        self.form = self.make_validated_form()
        self.validated = self.form.is_valid()
        self.form.save()

    def test_valid_form(self):
        self.assertTrue(self.validated)

    def test_create(self):
        self.assertTrue(User.objects.exists())

    def test_no_name(self):
        form = self.make_validated_form(first_name='')
        self.assertTrue(form.errors)
        msg = '* Informe seu nome.'
        self.assertEquals(form.errors['first_name'].as_text(), msg)

    def test_email_fatec(self):
        form = self.make_validated_form(username='xyx')
        self.assertTrue(form.errors)
        msg = '* Informe seu e-mail institucional.'
        self.assertEquals(form.errors['username'].as_text(), msg)

    def test_email_fatec2(self):
        form = self.make_validated_form(username='orlando@gmail.com')
        self.assertTrue(form.errors)
        msg = '* Informe seu e-mail institucional.'
        self.assertEquals(form.errors['username'].as_text(), msg)


    def test_password_not_optional(self):
        form = self.make_validated_form(password='')
        self.assertTrue(form.errors)
        msg = '* Este campo é obrigatório.'
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
        form = self.make_validated_form(username='')
        self.assertTrue(form.errors)
        msg = '* Informe o e-mail.'
        self.assertEquals(form.errors['username'].as_text(), msg)

    def test_email_in_use(self):
        form = self.make_validated_form()
        self.assertTrue(form.errors)
        msg = '* Um usuário com este nome de usuário já existe.'
        self.assertEquals(form.errors['username'].as_text(), msg)

    def make_validated_form(self, **kwargs):
        valid = dict(first_name='Orlando', last_name='Saraiva',
                     username='aluno_teste@fatec.sp.gov.br',
                     password='123mud@r')
        data = dict(valid, **kwargs)
        form = CadastroNovoAlunoForm(data)
        form.is_valid()
        return form
