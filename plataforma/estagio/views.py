from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse as r
from core.facade import area_trainee_coordinador, area_teacher, area_company
from estagio.forms import ConvenioForm, DocumentoEstagioForm
from estagio.forms import ProfessorConvenioForm, ProfessorDocumentoEstagioForm
from estagio.models import ConvenioModel, DocumentoEstagioModel
from plataforma import settings


@area_teacher
def listar_todos_convenios(request):
    convenios = ConvenioModel.objects.all().order_by('-created_at')
    context = {'media_url': settings.MEDIA_URL,
               'convenios': convenios}
    return render(request, 'listar_convenios.html', context)


@area_teacher
def pre_validar_convenio(request):
    if request.method == 'GET':
        convenios = ConvenioModel.objects.filter(observacao_professor='')
        context = {'media_url': settings.MEDIA_URL,
                   'convenios': convenios}
        return render(request, 'pre_validar_convenio.html', context)
    else:
        return HttpResponseRedirect(r('core:core_index_professor'))


@area_trainee_coordinador
def validar_convenio(request):
    if request.method == 'GET':
        return HttpResponseRedirect(r('core:core_index_professor'))
    else:
        id = request.POST.get('convenio_id', '')
        if id != '':
            convenio = ConvenioModel.objects.filter(pk=id)[0]
            context = {'media_url': settings.MEDIA_URL,
                       'convenio': convenio}
            return render(request, 'validar_convenio.html', context)
        else:
            return HttpResponseRedirect(r('core:core_index_professor'))


@area_trainee_coordinador
def pos_validar_convenio(request):
    if request.method == 'GET':
        return HttpResponseRedirect(r('core:core_index_professor'))
    else:
        id = request.POST.get('convenio_id', '')
        obs_padrao = 'Parecer Emitido pelo docente.'
        observacao = request.POST.get('observacao_professor', obs_padrao)
        aprovado = request.POST.get('aprovado_reprovado', '1')
        convenio = ConvenioModel.objects.filter(pk=id)[0]
        convenio.observacao_professor = observacao
        convenio.aprovado_professor = aprovado
        convenio.save()
        return render(request, 'pos_validar_convenio.html')


@area_teacher
def pre_validar_documento_estagio(request):
    if request.method == 'GET':
        documentos = DocumentoEstagioModel.objects.filter(
            observacao_professor='')
        context = {'media_url': settings.MEDIA_URL,
                   'documentos': documentos}
        return render(request, 'pre_validar_documento_estagio.html', context)
    else:
        return HttpResponseRedirect(r('core:core_index_professor'))


@area_trainee_coordinador
def professor_upload_convenio(request):
    if request.method == 'GET':
        context = {'form': ProfessorConvenioForm()}
        return render(request, 'professor_upload_convenio.html', context)
    else:
        form = ProfessorConvenioForm(request.POST, request.FILES)
        if form.is_valid():
            novo_nome = form.renomear_arquivo(form.files['documento'].name)
            form.files['documento'].name = novo_nome
            ConvenioModel.objects.create(**form.cleaned_data)
            return render(request, 'arquivo_enviado_pelo_professor.html')
        else:
            context = {'form': form}
            return render(request, 'professor_upload_convenio.html', context)


@area_trainee_coordinador
def professor_upload_documentos_estagio(request):
    if request.method == 'GET':
        context = {'form': ProfessorDocumentoEstagioForm()}
        return render(request, 'professor_upload_documentos_estagio.html', context)
    else:
        form = ProfessorDocumentoEstagioForm(request.POST, request.FILES)
        if form.is_valid():
            novo_nome = form.renomear_arquivo(form.files['documento'].name)
            form.files['documento'].name = novo_nome
            DocumentoEstagioModel.objects.create(**form.cleaned_data)
            return render(request, 'arquivo_enviado_pelo_professor.html')
        else:
            context = {'form': form}
            return render(request, 'professor_upload_documentos_estagio.html', context)



@area_trainee_coordinador
def validar_documento_estagio(request):
    if request.method == 'GET':
        return HttpResponseRedirect(r('core:core_index_professor'))
    else:
        id = request.POST.get('documento_id', '')
        if id != '':
            documento = DocumentoEstagioModel.objects.filter(pk=id)[0]
            context = {'media_url': settings.MEDIA_URL,
                       'documento': documento}
            return render(request, 'validar_documento_estagio.html', context)
        else:
            return HttpResponseRedirect(r('core:core_index_professor'))


@area_trainee_coordinador
def pos_validar_documento_estagio(request):
    if request.method == 'GET':
        return HttpResponseRedirect(r('core:core_index_professor'))
    else:
        id = request.POST.get('documento_id', '')
        if id != '':
            obs_padrao = 'Parecer Emitido pelo docente.'
            observacao = request.POST.get('observacao_professor', obs_padrao)
            aprovado = request.POST.get('aprovado_reprovado', '1')
            documento = DocumentoEstagioModel.objects.filter(pk=id)[0]
            documento.observacao_professor = observacao
            documento.aprovado_professor = aprovado
            documento.save()
            return render(request, 'pos_validar_documento_estagio.html')
        else:
            return HttpResponseRedirect(r('core:core_index_professor'))


@area_company
def upload_convenio(request):
    if request.method == 'GET':
        context = {'form': ConvenioForm(
            initial={"empresa": request.user.pk})}
        return render(request, 'upload_convenio.html', context)
    else:
        form = ConvenioForm(request.POST, request.FILES)
        if form.is_valid():
            novo_nome = form.renomear_arquivo(form.files['documento'].name)
            form.files['documento'].name = novo_nome
            ConvenioModel.objects.create(**form.cleaned_data)
            return render(request, 'arquivo_enviado_com_sucesso.html')
        else:
            context = {'form': form}
            return render(request, 'upload_convenio.html', context)


@area_company
def upload_documentos_estagio(request):
    if request.method == 'GET':
        context = {'form': DocumentoEstagioForm(
            initial={"empresa": request.user.pk})}
        return render(request, 'upload_documentos_estagio.html', context)
    else:
        form = DocumentoEstagioForm(request.POST, request.FILES)
        if form.is_valid():
            novo_nome = form.renomear_arquivo(form.files['documento'].name)
            form.files['documento'].name = novo_nome
            DocumentoEstagioModel.objects.create(**form.cleaned_data)
            return render(request, 'arquivo_enviado_com_sucesso.html')
        else:
            context = {'form': form}
            return render(request, 'upload_documentos_estagio.html', context)


@area_company
def convenio_por_empresa(request):
    if request.method == 'GET':
        id_user = request.user.pk
        convenios = ConvenioModel.objects.filter(empresa_id=id_user)
        context = {'media_url': settings.MEDIA_URL,
                   'convenios': convenios}
        return render(request, 'convenio_por_empresa.html', context)
    else:
        return HttpResponseRedirect(r('core:core_index_empresa'))


@area_company
def estagiarios_por_empresa(request):
    if request.method == 'GET':
        id_user = request.user.pk
        convenios = DocumentoEstagioModel.objects.filter(
            empresa_id=id_user).order_by('-created_at')
        context = {'media_url': settings.MEDIA_URL,
                   'convenios': convenios}
        return render(request, 'estagiarios_por_empresa.html', context)
    else:
        return HttpResponseRedirect(r('core:core_index_empresa'))
