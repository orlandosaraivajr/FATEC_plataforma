from django.shortcuts import render, redirect
from core.decorators import area_student
from vitrine.forms import VitrineForm
from vitrine.models import VitrineModel
from rest_framework import generics
from .serializers import VitrineSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend


def showcase(request):
    alunos = VitrineModel.objects.get_alunos()
    return render(request, 'showcase.html', {'alunos': alunos})


def showcase_tipo_vaga(request, tipo_vaga):
    alunos = VitrineModel.objects.get_tipo_vaga(tipo_vaga)
    return render(request, 'showcase.html', {'alunos': alunos})


def showcase_tipo_curso(request, curso):
    alunos = VitrineModel.objects.get_tipo_curso(curso)
    return render(request, 'showcase.html', {'alunos': alunos})


@area_student
def cadastro(request):
    if request.method == 'GET':
        context = {'cabecalho': 'Plataforma FATEC - Módulo Vitrine',
            'form': VitrineForm(), 'user': request.user}
        return render(request, 'cadastro.html', context)
    else:
        form = VitrineForm(request.POST)
        if form.is_valid():
            VitrineModel.objects.filter(aluno_id=request.user.pk).delete()
            VitrineModel.objects.create(**form.cleaned_data)
            context = {'cabecalho': 'Plataforma FATEC - Módulo Vitrine',
                       'mensagem': 'Cadastro feito com sucesso'} 
            return render(request, 'cadastro_feito.html', context)
        else:
            context = {'form': form, 'user': request.user}
            return render(request, 'cadastro.html', context)


@area_student
def remover(request):
    if request.method == 'GET':
        cadastro = VitrineModel.objects.filter(aluno_id=request.user.pk)
        if cadastro:
            context = {'cadastro': cadastro[0],
                       'user': request.user}
            return render(request, 'remover.html', context)
        else:
            context = {'cabecalho': 'Você não possui registro ainda',
                       'form': VitrineForm(), 'user': request.user}
            return render(request, 'cadastro.html', context)
    else:
        VitrineModel.objects.filter(aluno_id=request.user.pk).delete()
        context = {'cabecalho': 'Plataforma FATEC - Módulo Vitrine',
                   'mensagem': 'Seu anúncio foi removido.'} 
        return render(request, 'cadastro_feito.html', context)

# API views here.
class VitrineList(generics.ListAPIView):
    
    queryset = VitrineModel.objects.get_alunos()
    serializer_class = VitrineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo_vaga']

class VitrineListVaga(generics.ListAPIView):
    
    # queryset = VitrineModel.objects.get_alunos()
    serializer_class = VitrineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo_vaga']
    def get_queryset(self):
        tipo = self.kwargs['tipo']
        queryset = VitrineModel.objects.get_tipo_vaga(tipo)
        return queryset