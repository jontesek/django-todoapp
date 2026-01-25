from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Task

USER_NAME = "testuser"
USER_PASSWORD = "password123"  # noqa: S105
USER_B_NAME = "otheruser"


class TaskPermissionsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USER_NAME, password=USER_PASSWORD)
        self.user_b = User.objects.create_user(username=USER_B_NAME, password=USER_PASSWORD)
        self.root_url = reverse("tasks-all")

    def test_anonymous_user_is_banned(self):
        response = self.client.get(self.root_url)
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_can_access(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.root_url)
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_see_others_task(self):
        task_b = Task.objects.create(title="User B Task", user=self.user_b)
        self.client.force_authenticate(self.user)
        url = reverse("task-detail", kwargs={"pk": task_b.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_edit_others_task(self):
        # User 2 creates a task
        task_b = Task.objects.create(title="User B Task", user=self.user_b)

        # Log in as User A
        self.client.force_authenticate(self.user)

        # Try to edit User B's task
        edit_url = reverse("task-detail", kwargs={"pk": task_b.pk})
        response = self.client.patch(edit_url, {"title": "Hacked Title"})

        # Assert permission denied
        self.assertEqual(response.status_code, 403)

        # Verify the database didn't change
        task_b.refresh_from_db()
        self.assertEqual(task_b.title, "User B Task")


class TaskHierarchyTest(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username=USER_NAME, password=USER_PASSWORD)
        # Create tasks
        self.task_1 = Task.objects.create(title="Wake up", user=self.user)
        self.task_2 = Task.objects.create(title="Morning routine", user=self.user)
        self.task_3 = Task.objects.create(title="Make fruit tea", parent=self.task_2, user=self.user)
        self.task_4 = Task.objects.create(title="Brew hot water", parent=self.task_3, user=self.user)
        # Login with the user
        self.client.force_authenticate(user=self.user)

    def test_only_root_tasks(self):
        response = self.client.get(reverse("only-root-tasks"))
        self.assertEqual(len(response.data), 2)

    def test_direct_subtasks(self):
        url = reverse("direct-subtasks", kwargs={"pk": self.task_2.pk})
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

    def test_subtasks_tree(self):
        url = reverse("subtasks-tree", kwargs={"pk": self.task_2.pk})
        response_data = self.client.get(url).data

        subtask_1 = response_data[0]
        subsubtask_1 = subtask_1["subtasks"][0]

        self.assertEqual(subtask_1["id"], self.task_3.pk)
        self.assertEqual(subsubtask_1["id"], self.task_4.pk)

    def test_no_self_parent(self):
        payload = {"parent": self.task_1.pk}
        url = reverse("task-detail", kwargs={"pk": self.task_1.pk})
        response = self.client.patch(url, data=payload)
        self.assertEqual(response.status_code, 400)

    def test_no_cycle(self):
        payload = {"parent": self.task_4.pk}
        url = reverse("task-detail", kwargs={"pk": self.task_2.pk})
        response = self.client.patch(url, data=payload)
        self.assertEqual(response.status_code, 400)
