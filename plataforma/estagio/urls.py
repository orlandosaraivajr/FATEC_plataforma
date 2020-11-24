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
     path('listar_termos_compromisso_estagio',
          views.listar_termos_compromisso_estagio,
         name='listar_termos_compromisso_estagio'),
     path('listar_planos_de_atividades', views.listar_planos_de_atividades,
         name='listar_planos_de_atividades'),
     path('listar_termo_aditivo', views.listar_termo_aditivo,
         name='listar_termo_aditivo'),
     path('listar_rescisao_de_contrato', views.listar_rescisao_de_contrato,
         name='listar_rescisao_de_contrato'),
     path('listar_ficha_avaliacao_estagiario', views.listar_ficha_avaliacao_estagiario,
         name='listar_ficha_avaliacao_estagiario'),
     path('listar_relatorio_parcial_estagio', views.listar_relatorio_parcial_estagio,
         name='listar_relatorio_parcial_estagio'),
     path('listar_relatorio_final_estagio', views.listar_relatorio_final_estagio,
         name='listar_relatorio_final_estagio'),
]
urlpatterns += urlpatterns_empresa
urlpatterns += urlpatterns_professor
