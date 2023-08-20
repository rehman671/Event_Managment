from django.urls import reverse
from rest_framework.test import APITestCase

from user.tests import UserTestSetup

from .models import EventModel


class EventTestSetup(APITestCase):
    def setUp(self):
        self.pk = 1
        self.addevent_url = reverse("event-list")
        self.listevent_url = reverse("event-list")
        # self.attendevent_url = reverse('event-attend')

        self.event_data = {
            "title": "Test Event",
            "description": "TestEvent Desc",
            "date": "2023-8-20",
            "location": "Karachi",
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class EventTest(EventTestSetup, UserTestSetup):
    def test_create_event(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {
            "username": self.sign_user_data["username"],
            "password": self.sign_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        token = response.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = self.client.post(self.addevent_url, self.event_data, format="json")
        self.assertEqual(res.status_code, 201)

    def test_get_all_event(self):
        res = self.client.get(self.listevent_url, format="json")
        self.assertEqual(res.status_code, 200)

    def test_update_event_without_owner(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {
            "username": self.sign_user_data["username"],
            "password": self.sign_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        token = response.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        res = self.client.post(self.addevent_url, self.event_data, format="json")

        second_user = {
            "username": "test2",
            "email": "test2@gmail.com",
            "password": "test123",
            "phone_number": "+1 202-918-2132",
        }
        self.client.post(self.signup_url, second_user, format="json")
        login_data = {
            "username": second_user["username"],
            "password": second_user["password"],
        }
        response2 = self.client.post(self.login_url, login_data, format="json")
        token2 = response2.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")
        model_data = res.data["title"]
        model_data = EventModel.objects.get(title=model_data)
        self.event_data["title"] = "Changed Title"
        update_res = self.client.put(
            reverse("event-detail", args=[model_data.eid]),
            self.event_data,
            format="json",
        )
        self.assertEqual(update_res.status_code, 403)

    def test_update_event_with_owner(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {
            "username": self.sign_user_data["username"],
            "password": self.sign_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        token = response.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = self.client.post(self.addevent_url, self.event_data, format="json")
        model_data = res.data["title"]
        model_data = EventModel.objects.get(title=model_data)
        self.event_data["title"] = "Changed Title"
        update_res = self.client.put(
            reverse("event-detail", args=[model_data.eid]),
            self.event_data,
            format="json",
        )
        self.assertEqual(update_res.status_code, 200)

    def test_delete_event_without_owner(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {
            "username": self.sign_user_data["username"],
            "password": self.sign_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        token = response.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        res = self.client.post(self.addevent_url, self.event_data, format="json")
        model_data = res.data["title"]
        model_data = EventModel.objects.get(title=model_data)
        second_user = {
            "username": "test2",
            "email": "test2@gmail.com",
            "password": "test123",
            "phone_number": "+1 202-918-2132",
        }
        self.client.post(self.signup_url, second_user, format="json")
        login_data = {
            "username": second_user["username"],
            "password": second_user["password"],
        }
        response2 = self.client.post(self.login_url, login_data, format="json")
        token2 = response2.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")
        final_res = self.client.delete(reverse("event-detail", args=[model_data.eid]), format="json")
        self.assertEqual(final_res.status_code, 403)

    def test_delete_event_with_owner(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {
            "username": self.sign_user_data["username"],
            "password": self.sign_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        token = response.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = self.client.post(self.addevent_url, self.event_data, format="json")
        model_data = res.data["title"]
        model_data = EventModel.objects.get(title=model_data)
        final_res = self.client.delete(reverse("event-detail", args=[model_data.eid]), format="json")
        self.assertEqual(final_res.status_code, 204)

    def test_attend_event_doesnot_exist(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {
            "username": self.sign_user_data["username"],
            "password": self.sign_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        token = response.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.client.post(self.addevent_url, self.event_data, format="json")
        second_user = {
            "username": "test2",
            "email": "test2@gmail.com",
            "password": "test123",
            "phone_number": "+1 202-918-2132",
        }
        self.client.post(self.signup_url, second_user, format="json")
        login_data = {
            "username": second_user["username"],
            "password": second_user["password"],
        }
        response2 = self.client.post(self.login_url, login_data, format="json")
        token2 = response2.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")
        attend_res = self.client.post(reverse("event-attend", args=[523]), format="json")
        self.assertEqual(attend_res.status_code, 404)

    def test_attend_event(self):
        self.client.post(self.signup_url, self.sign_user_data, format="json")
        login_data = {
            "username": self.sign_user_data["username"],
            "password": self.sign_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        token = response.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = self.client.post(self.addevent_url, self.event_data, format="json")
        data = res.data["title"]
        model_data = EventModel.objects.get(title=data)
        second_user = {
            "username": "test2",
            "email": "test2@gmail.com",
            "password": "test123",
            "phone_number": "+1 202-918-2132",
        }
        self.client.post(self.signup_url, second_user, format="json")
        login_data = {
            "username": second_user["username"],
            "password": second_user["password"],
        }
        response2 = self.client.post(self.login_url, login_data, format="json")
        token2 = response2.data["token"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")
        attend_res = self.client.post(reverse("event-attend", args=[model_data.eid]), format="json")
        self.assertEqual(attend_res.status_code, 200)
