from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from core.decorators import (area_student, area_teacher,
                             area_company, area_admin)
from core.functions import auth_request, register_student, authenticate
from django.contrib.auth.decorators import login_required
from core.forms import CadastroNovoAlunoForm


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        if auth_request(request):
            return redirect('core:home')
        else:
            return redirect('core:login')


def logout(request):
    auth_logout(request)
    return render(request, 'login.html')


@login_required
def home(request):
    context = {'user': request.user}
    return render(request, 'index.html', context)


@area_student
def index_aluno(request):
    context = {}
    return render(request, 'aluno_index.html', context)


@area_teacher
def index_professor(request):
    context = {}
    return render(request, 'professor_index.html', context)


@area_teacher
def perfil_professor(request):
    context = {}
    return render(request, 'professor_mudar_perfil.html', context)


@area_company
def index_empresa(request):
    context = {}
    return render(request, 'empresa_index.html', context)


@area_admin
def index_manutencao(request):
    context = {}
    return render(request, 'manutencao_index.html', context)


def equipe_fatec(request):
    context = {}
    return render(request, 'equipe_fatec.html', context)


def cadastro_novo_aluno(request):
    if request.method == 'GET':
        context = {'form': CadastroNovoAlunoForm()}
        return render(request, 'cadastro_novo_aluno.html', context)
    else:
        form = CadastroNovoAlunoForm(request.POST)
        if form.is_valid():
            register_student(**form.cleaned_data)
            return redirect('core:login')
        else:
            context = {'form': form}
            return render(request, 'cadastro_novo_aluno.html', context)