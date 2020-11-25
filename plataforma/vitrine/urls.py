from django.urls import path
from . import views

app_name = 'vitrine'

urlpatterns = [
    path('', views.showcase, name='showcase'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('remover', views.remover, name='remover'),
]
