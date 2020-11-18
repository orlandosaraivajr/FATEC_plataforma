from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from vitrine.models import VitrineModel
from django.core.exceptions import ValidationError


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
            'aluno': forms.HiddenInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'tipo_vaga': forms.Select(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'descricao': {
                'required': ("Você precisa nos contar algo sobre você."),
            },
            'linkedin': {
                'required': ("Você precisa colocar seu endereço do Linkedin"),
            }
        }

    def clean_linkedin(self):
        linkedin = self.cleaned_data['linkedin']
        if len(linkedin) == 0:
            raise ValidationError('Linkedin não pode ser vazio.')
        return linkedin
