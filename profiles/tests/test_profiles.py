# from rest_framework.test import  APITestCase ,APIClient
# from django.contrib.auth import get_user_model
# from rest_framework.authtoken.models import Token
# from ..models import Profile
# from django.urls import reverse

# class ProfileTest(APITestCase):
#     def setup(self):
#         self.client = APIClient()
#         self.profile = Profile.objects.create(
#             username="testuser",
#             first_name="test",
#             last_name="user",
#             email="testemail@example.com",
#             file=None,
#             type="customer"

#         )
#     def test_profile_creation(self):
#         url = reverse('profile')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

#     def test_profile_post(self):
#         pass