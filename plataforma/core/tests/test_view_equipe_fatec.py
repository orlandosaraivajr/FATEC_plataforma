from django.test import TestCase
from django.shortcuts import resolve_url as r

view_in_test = 'core:quem_somos'
template_in_test = 'equipe_fatec.html'


class equipe_fatec_Get(TestCase):
    def setUp(self):
        self.resp = self.client.get(r(view_in_test))
        self.resp2 = self.client.get(r(view_in_test), follow=True)

    def test_template(self):
        self.assertTemplateUsed(self.resp2, template_in_test)

    def test_200_template_home(self):
        self.assertEqual(200, self.resp.status_code)
        self.assertEqual(200, self.resp2.status_code)

    def test_html(self):
        tags = (
            ('Módulo Empresa', 1),
            ('Módulo Professor', 0),
            ('<div', 40),
            ('</div>', 40),
            ('<input', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)