from django.urls import reverse
from rest_framework.test import APITestCase


class TestSetup(APITestCase):
    def setUp(self):
        self.signup_url = reverse("user-signup")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.refresh_url = reverse("refresh")

        self.sign_user_data = {
            "username": "test",
            "email": "test@gmail.com",
            "password": "test123",
            "phone_number": "+1 202-918-2132",
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class CustomUserTest(TestSetup):
    def test_sign_user_fail(self):
        res = self.client.post(self.signup_url)
        self.assertEqual(res.status_code, 400)

    def test_sign_user(self):
        res = self.client.post(self.signup_url, self.sign_user_data, format="json")
        self.assertEqual(res.status_code, 201)

    def test_login_user_incorrect(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {"username": "abc", "password": self.sign_user_data["password"]}
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_login_user(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {
            "username": self.sign_user_data["username"],
            "password": self.sign_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")

        self.assertEqual(response.status_code, 200)

    def test_logout_user(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {
            "username": self.sign_user_data["username"],
            "password": self.sign_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")

        token = response.data["token"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        logout_data = {"refresh": response.data["token"]["refresh"]}
        logout_res = self.client.post(self.logout_url, logout_data, format="json")

        self.assertEqual(logout_res.status_code, 200)

    def test_refreshtoken(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {
            "username": self.sign_user_data["username"],
            "password": self.sign_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        refresh = response.data["token"]["refresh"]

        token = {"refresh": refresh}

        refresh_res = self.client.post(self.refresh_url, token, format="json")
        self.assertEqual(refresh_res.status_code, 200)
