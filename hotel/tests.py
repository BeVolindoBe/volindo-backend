# from json import dumps

# from django.test import TestCase, Client

# from rest_framework import status


# class HotelTestCase(TestCase):

#     client = Client()

#     def test_update_traveler_by_id(self):
#         data = {
#             'first_name': 'Juan'
#         }
#         response = self.client.patch('/users/{}/travelers/{}/'.format(self.agent_id, self.traveler_id), json=data)
#         print(dumps(response.json(), indent=4))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json()['first_name'], 'Juan')
