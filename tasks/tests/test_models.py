"""Unit tests for Task model."""

from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from tasks.models import Task


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="testpass123")

    def test_str_includes_title_and_course(self):
        task = Task.objects.create(
            user=self.user,
            title="Homework 1",
            due_date=date(2026, 3, 20),
            course="15-213",
        )
        self.assertIn("Homework 1", str(task))
        self.assertIn("15-213", str(task))

    def test_str_no_course_uses_placeholder(self):
        task = Task.objects.create(
            user=self.user,
            title="Read chapter",
            due_date=date(2026, 3, 20),
        )
        self.assertIn("No course", str(task))

    def test_ordering_by_due_date_then_created(self):
        t1 = Task.objects.create(
            user=self.user,
            title="Later",
            due_date=date(2026, 4, 1),
        )
        t2 = Task.objects.create(
            user=self.user,
            title="Sooner",
            due_date=date(2026, 3, 1),
        )
        tasks = list(Task.objects.filter(user=self.user))
        self.assertEqual(tasks[0].id, t2.id)
        self.assertEqual(tasks[1].id, t1.id)
