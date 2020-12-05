from datetime import datetime
from django.shortcuts import resolve_url as r
from django.test import TestCase
from django.contrib.auth import get_user_model

from core.facade import CreateTestUser
from core.models import User
from vitrine.models import VitrineModel, VitrineManager


class VitrineManagerTest(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.client.post(r(self.login_url), data)
        self.usuario = User.objects.all()[0]
        senha = '123mudar'
        self.__criar_anuncio('Aluno 1', 'aluno1@fatec.sp.gov.br', senha, 'Aluno 1 quer trabalho', '', 'https://github.com/fatecano01', 1, 0)
        self.__criar_anuncio('Aluno 2', 'aluno2@fatec.sp.gov.br', senha, 'Aluno 2 quer trabalho', '', 'https://github.com/fatecano02', 2, 0)
        self.__criar_anuncio('Aluno 3', 'aluno3@fatec.sp.gov.br', senha, 'Aluno 3 quer estágio', '', 'https://github.com/fatecano03', 1, 1)
        self.__criar_anuncio('Aluno 4', 'aluno4@fatec.sp.gov.br', senha, 'Aluno 4 quer estágio', '', 'https://github.com/fatecano04', 2, 1)
        self.__criar_anuncio('Aluno 5', 'aluno5@fatec.sp.gov.br', senha, 'Aluno 5 quer estágio ou trabalho', '', 'https://github.com/fatecano05', 1, 2)
        self.__criar_anuncio('Aluno 6', 'aluno6@fatec.sp.gov.br', senha, 'Aluno 6 quer estágio ou trabalho', '', 'https://github.com/fatecano06', 2, 2)
        
        self.manager = VitrineManager()

    def __criar_anuncio(self, nome, email, senha, descricao, linkedin, github, curso, tipo_vaga):
        User = get_user_model()
        usuario = User(
            username=email,
            email=email,
            password=senha,
            first_name=nome,
            last_name='Fatecano',
        )
        usuario.save()
        vitrine = VitrineModel(
            aluno=usuario,
            descricao=descricao,
            linkedin=linkedin,
            github=github,
            curso=curso,
            tipo_vaga=tipo_vaga,
        )
        vitrine.save()

    def test_todos(self):
        self.assertEquals(6, len(VitrineModel.objects.all()))
        
    def test_get_tipo_curso(self):
        self.assertEquals(3, len(self.manager.get_tipo_curso(1)))
        self.assertEquals(3, len(self.manager.get_tipo_curso(2)))

    def test_get_tipo_vaga(self):
        self.assertEquals(4, len(self.manager.get_tipo_vaga(0)))
        self.assertEquals(4, len(self.manager.get_tipo_vaga(1)))
        self.assertEquals(2, len(self.manager.get_tipo_vaga(2)))
        self.assertEquals(2, len(self.manager.get_tipo_vaga(3)))

    def test_get_alunos_estagio(self):
        self.assertEquals(4, len(self.manager.get_alunos_estagio()))
    
    def test_get_alunos_emprego(self):
        self.assertEquals(4, len(self.manager.get_alunos_emprego()))