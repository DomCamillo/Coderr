from rest_framework.test import  APITestCase ,APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



User = get_user_model()



from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import uuid

User = get_user_model()


class RegistrationTest(APITestCase):

    def test_registration(self):
        """Test: Neuen User registrieren
        uuid4 to ensure unique usernames/emails"""
        unique_id = str(uuid.uuid4())[:8]

        data = {
            "username": f"testuser_{unique_id}",
            "email": f"test_{unique_id}@mail.com",
            "password": "SecurePass123!",
            "repeated_password": "SecurePass123!",
            "type": "customer"
        }

        response = self.client.post('/api/registration/', data, format='json')


        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)


class LoginTest(APITestCase):

    def test_login(self):
        """Test: User login
        uuid4 to ensure unique usernames/emails"""

        unique_id = str(uuid.uuid4())[:8]
        username = f"loginuser_{unique_id}"
        password = "TestPassword123!"


        user = User.objects.create_user(
            username=username,
            email=f"login_{unique_id}@mail.com",
            password=password
        )

        data = {
            "username": username,
            "password": password
        }

        response = self.client.post('/api/login/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)