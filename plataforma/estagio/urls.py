from django.urls import path
from . import views

app_name = 'estagio'

urlpatterns = []

urlpatterns_empresa = [
    path('upload_convenio', views.upload_convenio,
         name='upload_convenio'),
    path('convenio_por_empresa', views.convenio_por_empresa,
         name='convenio_por_empresa'),
]
urlpatterns_professor = [
    path('validar_convenio', views.validar_convenio,
         name='validar_convenio'),
    path('listar_todos_convenios', views.listar_todos_convenios,
         name='listar_todos_convenios'), 
]
urlpatterns += urlpatterns_empresa
urlpatterns += urlpatterns_professor
