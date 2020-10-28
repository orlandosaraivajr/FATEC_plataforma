from django.urls import path
from . import views

app_name = 'manutencao'

urlpatterns = []

urlpatterns_empresa = [
    path('cadastro_empresa', views.cadastro_empresa,
         name='cadastro_empresa'),

]
urlpatterns_professor = [
    path('cadastro_professor', views.cadastro_professor,
         name='cadastro_professor'),
]
urlpatterns_aluno = [
    path('cadastro_aluno', views.cadastro_aluno,
         name='cadastro_aluno'),
]
urlpatterns_editar = [
        path('editar_usuario', views.editar_usuarios,
         name='editar_usuario'),
]
urlpatterns += urlpatterns_empresa
urlpatterns += urlpatterns_professor
urlpatterns += urlpatterns_aluno
urlpatterns += urlpatterns_editar
