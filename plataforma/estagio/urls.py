from django.urls import path
from . import views

app_name = 'estagio'

urlpatterns = [
    path('upload_convenio', views.upload_convenio,
         name='upload_convenio'),
    path('validar_convenio', views.validar_convenio,
         name='estagio_validar_convenio'),
]
