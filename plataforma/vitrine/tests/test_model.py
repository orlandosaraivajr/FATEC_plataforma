from datetime import datetime
from django.shortcuts import resolve_url as r
from django.test import TestCase

from core.facade import CreateTestUser
from core.models import User
from vitrine.models import VitrineModel


class VitrineModelTest(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_student()
        self.client.post(r(self.login_url), data)
        self.student = User.objects.all()[0]
        self.vitrine = VitrineModel(
            aluno=self.student,
            descricao='nenhuma descrição',
            linkedin='http://linkedin.com/maeliseu/',
            github='http://github.com/maeliseu/',
            curso='1',
            tipo_vaga='2',
        )
        self.vitrine.save()

    def test_create(self):
        self.assertTrue(User.objects.exists())
        self.assertTrue(VitrineModel.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.vitrine.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.vitrine.updated_at, datetime)

    def test_tipo_vaga(self):
        self.assertEquals(self.vitrine.tipo_vaga, '2')

    def test_curso(self):
        self.assertEquals(self.vitrine.curso, '1')

    def test_linkedin(self):
        self.assertEquals(self.vitrine.linkedin, 'http://linkedin.com/maeliseu/')

    def test_github(self):
        self.assertEquals(self.vitrine.github, 'http://github.com/maeliseu/')

    def test_descricao(self):
        self.assertEqual(self.vitrine.descricao, 'nenhuma descrição')

    def test_estudante(self):
        self.assertEqual(self.vitrine.aluno.id, self.student.pk)