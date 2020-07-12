from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(verbose_name='Estudante', default=False)
    is_teacher = models.BooleanField(verbose_name='Professor', default=False)
    is_trainee_coordinator = models.BooleanField(
        verbose_name='Coodenador de Estágio', default=False)
    is_company = models.BooleanField(verbose_name='Empresa', default=False)

    def __str__(self):
        if self.first_name == '':
            return self.email
        return self.first_name
    
    class Meta:
        verbose_name_plural = 'Usuários'
        verbose_name = 'Usuário'
