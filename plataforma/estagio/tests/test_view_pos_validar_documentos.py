from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.shortcuts import resolve_url as r
from core.models import User
from core.facade import CreateTestUser
from estagio.models import DocumentoEstagioModel
from plataforma import settings

TINY_GIF = settings.TINY_GIF
view_in_test = 'estagio:pos_validar_documento_estagio'
template_in_test = 'pos_validar_documento_estagio.html'


class pos_validar_documento_NoAuthGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_template_home(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class pos_validar_documento_Get(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test), follow=True)
        self.resp2 = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'professor_index.html')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(302, self.resp2.status_code)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class pos_validar_documento_Post(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        self.documento = DocumentoEstagioModel(
            empresa=User.objects.all()[0],
            nome_aluno='José da Silva',
            curso_fatec=0,
            tipo_documento=0,
            observacao='nenhuma observação',
            documento=SimpleUploadedFile('tiny.pdf', TINY_GIF)
        )
        self.documento.save()
        data = {'documento_id': self.documento.pk,
                'observacao_professor': 'Parecer Favorável',
                'aprovado_reprovado': '1'}
        self.resp = self.client.post(r(view_in_test), data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_observacao_professor(self):
        valor = DocumentoEstagioModel.objects.filter(
            pk=self.documento.pk)[0]
        self.assertEqual(
            valor.observacao_professor, 'Parecer Favorável')

    def test_saved_aprovado(self):
        alterado = DocumentoEstagioModel.objects.filter(
            pk=self.documento.pk)[0]
        self.assertTrue(alterado.aprovado_professor)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class pos_validar_documento_Post_2(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        self.documento = DocumentoEstagioModel(
            empresa=User.objects.all()[0],
            nome_aluno='José da Silva',
            curso_fatec=0,
            tipo_documento=0,
            observacao='nenhuma observação',
            documento=SimpleUploadedFile('tiny.pdf', TINY_GIF)
        )
        self.documento.save()
        data = {'documento_id': self.documento.pk}
        self.resp = self.client.post(r(view_in_test), data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_observacao_professor(self):
        valor = DocumentoEstagioModel.objects.filter(pk=self.documento.pk)[0]
        self.assertEqual(
            valor.observacao_professor, 'Parecer Emitido pelo docente.')

    def test_saved_aprovado(self):
        valor = DocumentoEstagioModel.objects.filter(pk=self.documento.pk)[0]
        self.assertTrue(valor.aprovado_professor)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class pos_validar_documento_professor_Post(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.resp = self.client.post(r('core:login'), data)
        self.documento = DocumentoEstagioModel(
            empresa=User.objects.all()[0],
            nome_aluno='José da Silva',
            curso_fatec=0,
            tipo_documento=0,
            observacao='nenhuma observação',
            documento=SimpleUploadedFile('tiny.pdf', TINY_GIF)
        )
        self.documento.save()
        data = {'documento_id': self.documento.pk}
        self.resp = self.client.post(r(view_in_test), data)

    def test_200_or_302(self):
        self.assertEqual(302, self.resp.status_code)


class pos_validar_documento_Post_Fail_id_null(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_trainee_coordinator()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test), follow=True)
        self.resp2 = self.client.post(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'professor_index.html')
        self.assertTemplateUsed(self.resp, 'rodape.html')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(302, self.resp2.status_code)
