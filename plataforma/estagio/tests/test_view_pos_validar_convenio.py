from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.shortcuts import resolve_url as r
from core.facade import User
from core.facade import CreateTestUser
from estagio.models import ConvenioModel
from plataforma import settings

TINY_GIF = settings.TINY_GIF
view_in_test = 'estagio:pos_validar_convenio'
template_in_test = 'pos_validar_convenio.html'


class pos_validar_convenio_NoAuthGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, 'login.html')

    def test_200_template_home(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class pos_validar_convenio_Get(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.resp = self.client.post(r('core:login'), data)
        self.resp = self.client.get(r(view_in_test), follow=True)
        self.resp2 = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'professor_index.html')

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(302, self.resp2.status_code)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class pos_validar_convenio_Post(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.resp = self.client.post(r('core:login'), data)
        self.convenio = ConvenioModel(
            empresa=User.objects.all()[0],
            observacao='nenhuma observação',
            documento=SimpleUploadedFile('tiny.pdf', TINY_GIF)
        )
        self.convenio.save()
        data = {'convenio_id': self.convenio.pk,
                'observacao_professor': 'Parecer Favorável',
                'aprovado_reprovado': '1'}
        self.resp = self.client.post(r(view_in_test), data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_observacao_professor(self):
        alterado = ConvenioModel.objects.filter(pk=self.convenio.pk)[0]
        self.assertEqual(
            alterado.observacao_professor, 'Parecer Favorável')

    def test_saved_aprovado(self):
        alterado = ConvenioModel.objects.filter(pk=self.convenio.pk)[0]
        self.assertTrue(alterado.aprovado_professor)


@override_settings(DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage')
class pos_validar_convenio_Post_2(TestCase, CreateTestUser):
    def setUp(self):
        data = self.create_user_teacher()
        self.resp = self.client.post(r('core:login'), data)
        self.convenio = ConvenioModel(
            empresa=User.objects.all()[0],
            observacao='nenhuma observação',
            documento=SimpleUploadedFile('tiny.pdf', TINY_GIF)
        )
        self.convenio.save()
        data = {'convenio_id': self.convenio.pk}
        self.resp = self.client.post(r(view_in_test), data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_or_302(self):
        self.assertEqual(200, self.resp.status_code)

    def test_saved_observacao_professor(self):
        alterado = ConvenioModel.objects.filter(pk=self.convenio.pk)[0]
        self.assertEqual(
            alterado.observacao_professor, 'Parecer Emitido pelo docente.')

    def test_saved_aprovado(self):
        alterado = ConvenioModel.objects.filter(pk=self.convenio.pk)[0]
        self.assertTrue(alterado.aprovado_professor)
