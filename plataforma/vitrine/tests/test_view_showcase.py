
from django.shortcuts import resolve_url as r
from django.test import TestCase

url_testada = 'vitrine:showcase'


class vitrineGetOk(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(url_testada))
        self.resp2 = self.client.get(r(url_testada), follow=True)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp2, 'showcase.html')

    def test_200_or_302_responses(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)