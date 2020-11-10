from django.urls import path
from . import views

app_name = 'estagio'

urlpatterns = []

urlpatterns_empresa = [
    path('upload_convenio', views.upload_convenio,
         name='upload_convenio'),
    path('upload_documentos_estagio', views.upload_documentos_estagio,
         name='upload_documentos_estagio'),
    path('convenio_por_empresa', views.convenio_por_empresa,
         name='convenio_por_empresa'),
    path('estagiarios_por_empresa', views.estagiarios_por_empresa,
         name='estagiarios_por_empresa'),
]
urlpatterns_professor = [
    path('professor_upload_documentos_estagio',
         views.professor_upload_documentos_estagio,
         name='professor_upload_documentos_estagio'),
    path('professor_upload_convenio', views.professor_upload_convenio,
         name='professor_upload_convenio'),
    path('pre_validar_convenio', views.pre_validar_convenio,
         name='pre_validar_convenio'),
    path('validar_convenio', views.validar_convenio,
         name='validar_convenio'),
    path('pos_validar_convenio', views.pos_validar_convenio,
         name='pos_validar_convenio'),
    path('listar_todos_convenios', views.listar_todos_convenios,
         name='listar_todos_convenios'),
    path('pre_validar_documento_estagio', views.pre_validar_documento_estagio,
         name='pre_validar_documento_estagio'),
    path('validar_documento_estagio', views.validar_documento_estagio,
         name='validar_documento_estagio'),
    path('pos_validar_documento_estagio', views.pos_validar_documento_estagio,
         name='pos_validar_documento_estagio'),
]
urlpatterns += urlpatterns_empresa
urlpatterns += urlpatterns_professor
