import hashlib
import random
from django import forms
from django.forms import ModelForm
from estagio.models import ConvenioModel


class ConvenioForm(ModelForm):
    class Meta:
        model = ConvenioModel
        fields = ('empresa', 'documento', 'observacao')
        labels = {
            'documento': 'Arquivo',
            'observacao': 'Observação',
        }
        widgets = {
            'empresa': forms.HiddenInput(),
            'observacao': forms.Textarea(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'empresa': {
                'required': ("Informe ID da empresa."),
            },
            'documento': {
                'required': ("Informe um arquivo."),
            }
        }

    def renomear_arquivo(self, nome):
        sufixo = nome[-5:]
        nome = hashlib.sha256(
            str(random.getrandbits(256)).encode('utf-8')).hexdigest()
        nome = nome + sufixo
        return nome

    def clean_observacao(self):
        return self.cleaned_data['observacao'].upper()
