from django.shortcuts import render
from core.decorators import area_student
from vitrine.forms import VitrineForm


def showcase(request):
    return render(request, 'showcase.html')

@area_student
def cadastro(request):
    context = {'form':VitrineForm()}
    return render(request, 'cadastro.html', context)