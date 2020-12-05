
from django.shortcuts import resolve_url as r
from django.test import TestCase

url_testada = 'vitrine:showcase_tipo_curso'


class vitrine_tipo_curso_Get_0_Ok(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(url_testada, 0))
        self.resp2 = self.client.get(r(url_testada, 0), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'showcase.html')

    def test_200_or_302_responses(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)


class vitrine_tipo_curso_Get_1_Ok(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(url_testada, 1))
        self.resp2 = self.client.get(r(url_testada, 1), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'showcase.html')

    def test_200_or_302_responses(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)

class vitrine_tipo_curso_Get_2_Ok(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(url_testada, 2))
        self.resp2 = self.client.get(r(url_testada, 2), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'showcase.html')

    def test_200_or_302_responses(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)