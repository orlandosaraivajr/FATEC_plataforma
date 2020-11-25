from django.shortcuts import render
from core.decorators import area_student
from vitrine.forms import VitrineForm
from vitrine.models import VitrineModel

def showcase(request):
    return render(request, 'showcase.html')

@area_student
def cadastro(request):
    if request.method == 'GET':
        context = {'form':VitrineForm(), 'user':request.user}
        return render(request, 'cadastro.html', context)
    else:
        form = VitrineForm(request.POST)
        if form.is_valid():
            VitrineModel.objects.create(**form.cleaned_data)
            return render(request, 'aluno_index.html')
        else:
            context = {'form': form, 'user':request.user}
            return render(request, 'cadastro.html', context)
