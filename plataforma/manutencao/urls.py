from django.urls import path
from . import views

app_name = 'manutencao'

urlpatterns = []

urlpatterns_empresa = [
    path('cadastro_empresa', views.cadastro_empresa,
         name='cadastro_empresa'),
    path('editar_empresa', views.editar_empresa,
         name='editar_empresa'),
]
urlpatterns_professor = [
    path('cadastro_professor', views.cadastro_professor,
         name='cadastro_professor'),
    path('alterar_professor', views.alterar_professor,
         name='alterar_professor'),
]
urlpatterns += urlpatterns_empresa
urlpatterns += urlpatterns_professor
