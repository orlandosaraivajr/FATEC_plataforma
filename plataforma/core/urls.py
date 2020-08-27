from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('quem_somos', views.equipe_fatec, name='quem_somos'),
]
urlpatterns_aluno = [
    path('index_aluno', views.index_aluno, name='core_index_aluno'),
]

urlpatterns_professor = [
    path('index_professor', views.index_professor,
    name='core_index_professor'),
    path('perfil_professor', views.perfil_professor, name='perfil_professor'),
]
urlpatterns_empresa = [
    path('index_empresa', views.index_empresa, name='core_index_empresa'),
]
urlpatterns += urlpatterns_aluno
urlpatterns += urlpatterns_empresa
urlpatterns += urlpatterns_professor
