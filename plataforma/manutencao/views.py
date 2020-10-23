from django.shortcuts import render
from core.decorators import area_admin
from manutencao.forms import UserCreateForm, UserEditForm
from core.functions import register_new_company, update_user, register_new_teacher


@area_admin
def cadastro_empresa(request):
    if request.method == 'GET':
        context = {'form': UserCreateForm()}
        return render(request, 'cadastro_empresa.html', context)
    else:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            register_new_company(email, password)
        else:
            context = {'form': form}
            return render(request, 'cadastro_empresa.html', context)
        context = {'title': 'Cadastrar Empresas na plataforma FATEC',
                   'msg': 'Cadastro da empresa realizada com sucesso !',}
        return render(request, 'cadastro_edicao_concluido.html', context)


@area_admin
def editar_usuarios(request):
    if request.method == 'GET':
        context = {'form': UserEditForm()}
        return render(request, 'editar_usuarios.html', context)
    else:
        form = UserEditForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('user_id', '')
            password = form.cleaned_data.get('password', '')
            first_name = form.cleaned_data.get('first_name', '')
            last_name = form.cleaned_data.get('last_name', '')
            update_user(id=user_id.pk, password=password,
                        first_name=first_name, last_name=last_name)

        else:
            context = {'form': form}
            return render(request, 'editar_usuarios.html', context)
        context = {'title': 'Editar Empresas na plataforma FATEC',
                   'msg': 'Edição da empresa realizada com sucesso !',}
        return render(request, 'cadastro_edicao_concluido.html', context)



@area_admin
def cadastro_professor(request):
    if request.method == 'GET':
        context = {'form': UserCreateForm()}
        return render(request, 'cadastro_professor.html', context)
    else:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            register_new_teacher(email, password)
        else:
            context = {'form': form}
            return render(request, 'cadastro_professor.html', context)
        context = {'title': 'Cadastrar Professores na plataforma FATEC',
                   'msg': 'Cadastro de docente realizado com sucesso !',}
        return render(request, 'cadastro_edicao_concluido.html', context)
