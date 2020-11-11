from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from vitrine.models import VitrineModel


class VitrineForm(ModelForm):
    class Meta:
        model = VitrineModel
        fields = ('aluno', 'descricao', 'linkedin', 'github', 'curso', 'tipo_vaga')
        labels = {
            'aluno': 'Nome',
            'descricao': 'Descricao',
            'linkedin':'Link Linkedin',
            'github':'Link Github',
            'curso':'Curso',
            'tipo_vaga':'Tipo da Vaga'
        }
        widgets = {
            'aluno': forms.EmailInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'aluno': {
                'required': ("Preencha o aluno."),
            },
            'descricao': {
                'required': ("Informe a senha provisória."),
            }
        }