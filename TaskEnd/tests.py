from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .models import Task


class TaskAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser",
            password="test12345"
        )

        self.task = Task.objects.create(
            title="Learn Django",
            priority="medium",
            owner=self.user
        )

    def test_get_tasks(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        data = {
            "title": "New Task",
            "priority": "high",
            "completed": False,
            "deadline": None,
            "owner": self.user.id
        }

        response = self.client.post(
            "/api/tasks/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "New Task")

    def test_get_single_task(self):
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Learn Django")

    def test_update_task(self):
        data = {
            "title": "Updated Task",
            "priority": "low",
            "completed": True,
            "deadline": None,
            "owner": self.user.id
        }

        response = self.client.put(
            f"/api/tasks/{self.task.id}/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Updated Task")

    def test_delete_task(self):
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, 204)
