from django.urls import reverse
from rest_framework import status
from codeqaapi.tests import BaseTestCase


class AuthenticationTestCase(BaseTestCase):
    """Ensure user can signin
    """

    def test_user_can_signin(self):
        url = reverse('auth:signin')
        response = self.post_data(
            url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')

    def test_user_signin_fails_with_wrong_credentials(self):
        url = reverse('auth:signin')
        response = self.post_data(
            url, {'username': 'wrong', 'password': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register(self):
        url = reverse('auth:signup')
        response = self.post_data(
            url, {'user': {'username': 'solo',
                           'password': 'password', 'email': 'solo@codeqa.io'}}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'user')

    def test_user_cannot_register_with_used_email(self):
        url = reverse('auth:signup')
        response = self.post_data(
            url, {'user': {'username': 'solo',
                           'password': 'password', 'email': self.email}}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(response.data['errors']
                      ['email'][0], 'Email already in use')
