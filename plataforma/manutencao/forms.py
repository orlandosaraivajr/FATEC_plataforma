from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from core.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'E-mail:',
            'password': 'Senha provisória:',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'email': {
                'required': ("Preencha o e-mail."),
            },
            'password': {
                'required': ("Informe a senha provisória."),
            }
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == '':
            raise ValidationError(
                'Informe o e-mail. Não deixe este campo em branco')
        if len(User.objects.filter(email__exact=email)) > 0:
            raise ValidationError(
                'Este e-mail está em uso. Digite outro e-mail.')
        return self.cleaned_data['email']

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
