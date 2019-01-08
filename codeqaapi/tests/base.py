from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):
    """Base test case
    """

    def setUp(self):
        self.username = 'myuser'
        self.password = 'mypassword'
        self.email = 'myemail@codeqa.io'

        self.user = self.user = User.objects.create_user(
            self.username, self.email, self.password)

    def login(self, data):
        """Login a user with the given data
        """
        self.client.login(**data)

    def post_data(self, url, data):
        """Make a post request to url with data """
        return self.client.post(url, data, format='json')

    def tearDown(self):
        user = User.objects.filter(username=self.username).first()
        if user:
            user.delete()
