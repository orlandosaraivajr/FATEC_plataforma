from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import resolve_url as r
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from estagio.models import DocumentoEstagioModel, DocumentoEstagioManager
from core.facade import CreateTestUser
from core.facade import User
from plataforma import settings

TINY_PDF = settings.TINY_PDF


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class DocumentoEstagioManagerTest(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_company()
        self.client.post(r(self.login_url), data)
        self.usuario = User.objects.all()[0]
        self.__criar_arquivo(0, 'termo de compromisso de estágio')
        self.__criar_arquivo(0, 'termo de compromisso de estágio 2')
        self.__criar_arquivo(1, 'plano de atividade')
        self.__criar_arquivo(2, 'termo aditivo 1')
        self.__criar_arquivo(2, 'termo aditivo 2')
        self.__criar_arquivo(2, 'termo aditivo 3')
        self.__criar_arquivo(3, 'rescisão de contrato 1')
        self.__criar_arquivo(3, 'rescisão de contrato 2')
        self.__criar_arquivo(3, 'rescisão de contrato 3')
        self.__criar_arquivo(3, 'rescisão de contrato 4')
        self.__criar_arquivo(4, 'Ficha de avaliação do estagiário')
        self.__criar_arquivo(5, 'Relatório Parcial de Estágio 1')
        self.__criar_arquivo(5, 'Relatório Parcial de Estágio 2')
        self.__criar_arquivo(6, 'Relatório Final de Estágio 1')
        self.__criar_arquivo(6, 'Relatório Final de Estágio 2')
        self.__criar_arquivo(6, 'Relatório Final de Estágio 3')
        self.manager = DocumentoEstagioManager()

    def __criar_arquivo(self, tipo_documento, observacao):
        self.documento = DocumentoEstagioModel(
            empresa=self.usuario,
            tipo_documento=tipo_documento,
            observacao=observacao,
            documento=SimpleUploadedFile('tiny.pdf', TINY_PDF.read())
        )
        self.documento.save()

    def test_todos(self):
        self.assertEquals(16, len(DocumentoEstagioModel.objects.all()))
        
    def test_todos_planos_de_atividades(self):
        self.assertEquals(1, len(self.manager.planos_de_atividades()))

    def test_todos_termos_compromisso_estagio(self):
        self.assertEquals(2, len(self.manager.termos_compromisso_estagio()))

    def test_todos_termo_aditivo(self):
        self.assertEquals(3, len(self.manager.termos_aditivo()))

    def test_todos_rescisao_contrato(self):
        self.assertEquals(4, len(self.manager.rescisao_de_contrato()))

    def test_todos_ficha_avaliacao_estagiario(self):
        self.assertEquals(1, len(self.manager.ficha_avaliacao_estagiario()))

    def test_todos_relatorio_parcial_estagio(self):
        self.assertEquals(2, len(self.manager.relatorio_parcial_estagio()))

    def test_todos_relatorio_final_estagio(self):
        self.assertEquals(3, len(self.manager.relatorio_final_estagio()))