from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from notes.models import Category, Note


class CategoryViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="qwerty"
        )
        self.client.login(username="testuser", password="qwerty")

        self.category = Category.objects.create(
            user=self.user,
            name="Test Category",
            color="#FFFFFF",
        )

    def test_create_category(self):
        response = self.client.post(
            reverse("category"), {"name": "New Category", "color": "#FFFFFF"}
        )
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Category.objects.filter(name="New Category").exists())

    def test_update_category(self):
        response = self.client.post(
            reverse("category-update", kwargs={"category_id": self.category.id}),
            {"name": "New Category", "color": "#FFFFFF"},
        )
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertEquals(self.category.name, "New Category")

    def test_delete_category(self):
        response = self.client.post(
            reverse("category-delete", kwargs={"category_id": self.category.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(name="Test Category").exists())


class NotesListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="qwerty"
        )
        self.client.login(username="testuser", password="qwerty")
        self.category = Category.objects.create(
            user=self.user, name="Test Category", color="white"
        )
        self.note1 = Note.objects.create(
            user=self.user, text="Test Note 1", category=self.category
        )
        self.note2 = Note.objects.create(
            user=self.user, text="Test Note 2", category=self.category, archived=True
        )
        self.url = reverse("notes-list")

    def test_get_notes_list(self):
        response = self.client.get(reverse("notes-list"))
        self.assertEqual(response.status_code, 200)

    def test_create_note(self):
        response = self.client.post(
            reverse("notes-list"),
            {"text": "New Note", "category": "Test Category"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(text="New Note").exists())

    def test_get_notes_by_unauthorized_user(self):
        self.client.logout()
        response = self.client.get(reverse("notes-list"))
        self.assertEqual(response.status_code, 302)


class ArchiveNoteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.category = Category.objects.create(
            user=self.user, name="Test Category", color="white"
        )
        self.note = Note.objects.create(
            user=self.user, text="Test Note", category=self.category
        )
        self.url = reverse("get-archive")

    def test_get_archived_notes_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_toggle_note_archived_status(self):
        response = self.client.post(
            reverse("archive_note", kwargs={"note_id": self.note.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.note.refresh_from_db()
        self.assertTrue(self.note.archived)


class SearchNoteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.category = Category.objects.create(
            user=self.user, name="Test Category", color="white"
        )
        self.note1 = Note.objects.create(
            user=self.user, text="Test Note 1", category=self.category, archived=False
        )
        self.note2 = Note.objects.create(
            user=self.user, text="Test Note 2", category=self.category, archived=False
        )
        self.url = reverse("search")

    def test_search_notes(self):
        response = self.client.get(self.url + "?query=Test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note 1")
        self.assertContains(response, "Test Note 2")

    def test_search_notes_no_results(self):
        response = self.client.get(self.url + "?query=Nonexistent")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Note 1")
        self.assertNotContains(response, "Test Note 2")
