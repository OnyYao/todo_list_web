"""HTTP and API tests for tasks views."""

import json
from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase
from tasks.models import Task


class IndexAndAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="bob", password="secret123")

    def test_index_redirects_unauthenticated_to_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_index_renders_for_authenticated_user(self):
        self.client.login(username="bob", password="secret123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login_post_success_returns_json(self):
        response = self.client.post(
            "/login/",
            data=json.dumps({"username": "bob", "password": "secret123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data.get("redirect"), "/")

    def test_login_post_invalid_credentials(self):
        response = self.client.post(
            "/login/",
            data=json.dumps({"username": "bob", "password": "wrong"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json().get("success"))

    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(
            "/register/",
            data=json.dumps(
                {
                    "username": "carol",
                    "password": "pw123456",
                    "email": "carol@example.com",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get("success"))
        self.assertTrue(User.objects.filter(username="carol").exists())


class TaskApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="dave", password="pw123456")
        self.client.login(username="dave", password="pw123456")
        self.today = date.today()

    def test_api_tasks_requires_login(self):
        c = Client()
        response = c.get("/api/tasks/")
        self.assertEqual(response.status_code, 302)

    def test_api_tasks_lists_user_tasks(self):
        Task.objects.create(
            user=self.user,
            title="Essay",
            due_date=self.today,
            course="76-101",
        )
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload["tasks"]), 1)
        self.assertEqual(payload["tasks"][0]["title"], "Essay")
        self.assertEqual(payload["tasks"][0]["course"], "76-101")

    def test_api_tasks_today_filter(self):
        Task.objects.create(
            user=self.user,
            title="Due today",
            due_date=self.today,
        )
        Task.objects.create(
            user=self.user,
            title="Due later",
            due_date=date(2099, 1, 1),
        )
        response = self.client.get("/api/tasks/?today=1")
        self.assertEqual(response.status_code, 200)
        titles = [t["title"] for t in response.json()["tasks"]]
        self.assertEqual(titles, ["Due today"])

    def test_api_task_create(self):
        response = self.client.post(
            "/api/tasks/create/",
            data=json.dumps(
                {
                    "title": "Lab 3",
                    "description": "Finish buffer lab",
                    "due_date": self.today.isoformat(),
                    "course": "15-213",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertEqual(body["task"]["title"], "Lab 3")
        self.assertEqual(Task.objects.filter(user=self.user).count(), 1)

    def test_api_task_create_rejects_missing_title(self):
        response = self.client.post(
            "/api/tasks/create/",
            data=json.dumps({"due_date": self.today.isoformat()}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Title", response.json().get("error", ""))

    def test_api_task_update_and_delete(self):
        task = Task.objects.create(
            user=self.user,
            title="Old",
            due_date=self.today,
        )
        upd = self.client.put(
            f"/api/tasks/{task.id}/",
            data=json.dumps({"title": "New", "completed": True}),
            content_type="application/json",
        )
        self.assertEqual(upd.status_code, 200)
        self.assertTrue(upd.json()["task"]["completed"])
        task.refresh_from_db()
        self.assertEqual(task.title, "New")

        delete = self.client.delete(f"/api/tasks/{task.id}/delete/")
        self.assertEqual(delete.status_code, 200)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_api_task_not_found_other_user(self):
        other = User.objects.create_user(username="eve", password="pw")
        task = Task.objects.create(
            user=other,
            title="Private",
            due_date=self.today,
        )
        response = self.client.delete(f"/api/tasks/{task.id}/delete/")
        self.assertEqual(response.status_code, 404)

    def test_api_today_count(self):
        Task.objects.create(
            user=self.user,
            title="A",
            due_date=self.today,
            completed=False,
        )
        Task.objects.create(
            user=self.user,
            title="B",
            due_date=self.today,
            completed=True,
        )
        response = self.client.get("/api/tasks/today-count/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
