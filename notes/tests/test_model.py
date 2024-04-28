from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from notes.models import Category, CategoryColor, Note


class CategoryColorModelTest(TestCase):

    def test_color_code_validation(self):
        color = CategoryColor(color_code="#FFFFFF")
        color.full_clean()
        invalid_color = "invalid_color"
        with self.assertRaises(ValidationError):
            color = CategoryColor(color_code=invalid_color)
            color.full_clean()


class CategoryModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )

    def test_category_creation(self):
        color = CategoryColor.objects.create(color_code="#FFFFFF")
        category = Category.objects.create(
            user=self.user, name="Test Category", color=color
        )
        self.assertEqual(category.name, "Test Category")

    def test_category_creation_with_unique_name(self):
        category_color = CategoryColor.objects.create(color_code="#00FF00")
        Category.objects.create(
            user=self.user, name="Unique Category", color=category_color
        )
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                user=self.user, name="Unique Category", color=category_color
            )


from django.test import TestCase
from django.contrib.auth import get_user_model
from notes.models import Note, Category


class NoteModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        category_color = CategoryColor.objects.create(color_code="#FFFFFF")
        self.category = Category.objects.create(
            user=self.user, name="Test Category", color=category_color
        )

    def test_note_creation(self):
        note = Note.objects.create(
            user=self.user, text="Test note text", category=self.category
        )
        self.assertEqual(note.text, "Test note text")

    def test_archived_default_value(self):
        note = Note.objects.create(
            user=self.user, text="Test note text", category=self.category
        )
        self.assertFalse(note.archived)

    def test_ordering(self):
        note1 = Note.objects.create(
            user=self.user, text="First note", category=self.category
        )
        note2 = Note.objects.create(
            user=self.user, text="Second note", category=self.category
        )

        self.assertEqual(list(Note.objects.all()), [note2, note1])

    def test_category_set_null_on_delete(self):
        note = Note.objects.create(
            user=self.user, text="Test note text", category=self.category
        )
        self.category.delete()
        note.refresh_from_db()
        self.assertIsNone(note.category)
