from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from vitrine.views import VitrineList


class TestVitrineAPI(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = VitrineList.as_view()
        self.uri = '/api/vitrine/'

    def test_list(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
