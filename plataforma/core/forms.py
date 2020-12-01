from django import forms
from django.forms import ModelForm
from core.models import User
from django.core.exceptions import ValidationError


class CadastroNovoAlunoForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')
        labels = {
            'first_name': 'Nome:',
            'last_name': 'Sobrenome:',
            'username': 'E-mail institucional:',
            'password': 'Senha:',
        }
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'username': forms.EmailInput(),
            'password': forms.PasswordInput(),
        }
        error_messages = {
            'username': {
                'required': ("Informe o e-mail."),
            },
            'first_name': {
                'required': ("Informe seu nome."),
            },
            'last_name': {
                'required': ("Informe seu sobrenome."),
            }
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name == '':
            raise ValidationError(
                'Informe seu nome.')
        return self.cleaned_data['first_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.endswith('@fatec.sp.gov.br'):
            raise ValidationError('Informe seu e-mail institucional.')
        return self.cleaned_data['username']

    def clean_password(self):
        senha = self.cleaned_data['password']
        possui_numeros = False
        for n in list('1234567890'):
            if n in list(senha):
                possui_numeros = True
        if not possui_numeros:
            raise ValidationError(
                'A senha precisa ter pelo menos um número.')
        if len(senha) < 8:
            raise ValidationError(
                'A senha precisa ter pelo menos 8 caracteres.')
        return self.cleaned_data['password']