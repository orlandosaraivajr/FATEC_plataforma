from django.shortcuts import render
from core.decorators import area_admin
from manutencao.forms import UserForm
from core.functions import register_new_company


@area_admin
def cadastro_empresa(request):
    if request.method == 'GET':
        context = {'form': UserForm()}
        return render(request, 'cadastro_empresa.html', context)
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            register_new_company(email, password)
        else:
            context = {'form': form}
            return render(request, 'cadastro_empresa.html', context)
        return render(request, 'cadastro_empresa_concluido.html')


@area_admin
def editar_empresa(request):
    context = {}
    return render(request, 'manutencao_index.html', context)


@area_admin
def cadastro_professor(request):
    context = {}
    return render(request, 'manutencao_index.html', context)


@area_admin
def alterar_professor(request):
    context = {}
    return render(request, 'manutencao_index.html', context)
