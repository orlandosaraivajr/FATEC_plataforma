from rest_framework import status
from rest_framework.test import APITestCase
# from django.test import TestCase
from vitrine.models import VitrineModel
from vitrine.serializers import VitrineSerializer

class VitrineViewsTest(APITestCase):
    # @classmethod
    def setUpTestData(cls):
        # (1)         
        cls.vitrines = [VitrineModel.objects.create() for _ in range(3)]
        cls.vitrine = cls.vitrines[0]

    def test_can_browse_all_vitrines(self):
        # (2) 
        response = self.client.get(reverse("vitrines:vitrine-list"))

        # (3) 
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.vitrines), len(response.data))

        for vitrine in self.vitrines:
            # (4) 
            self.assertIn(
                VitrineSerializer(instance=vitrine).data,
                response.data
            )

    # def test_can_read_a_specific_vitrine(self):
    #     # (5) 
    #     response = self.VitrineModel.get(
    #         reverse("VitrineModels:VitrineModel-detail", args=[self.VitrineModel.id])
    #     )

    #     self.assertEquals(status.HTTP_200_OK, response.status_code)
    #     self.assertEquals(
    #         VitrineSerializer(instance=VitrineModel).data,
    #         response.data
    #     )