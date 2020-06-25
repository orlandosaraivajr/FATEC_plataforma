from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index_aluno', views.index_aluno, name='core_index_aluno'),
    path('index_professor', views.index_professor, name='core_index_professor'),
    path('index_empresa', views.index_empresa, name='core_index_empresa'),
]
