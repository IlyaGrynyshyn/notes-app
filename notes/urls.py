from django.urls import path
from .views import (
    NotesListView,
    NoteUpdateView,
    ArchiveNoteView,
    CategoryListView,
    CategoryUpdateView,
    SearchNoteView,
    FilterNotesView,
    NoteDeleteView,
    NoteUpdateView,
    CategoryDeleteView,
)

urlpatterns = [
    path("", NotesListView.as_view(), name="notes-list"),
    path("category/", CategoryListView.as_view(), name="category"),
    path(
        "category/<int:category_id>",
        CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "category/<int:category_id>/delete",
        CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    path("note/<int:note_id>/edit/", NoteUpdateView.as_view(), name="note-update"),
    path("note/<int:note_id>/delete/", NoteDeleteView.as_view(), name="note-delete"),
    path("archive/", ArchiveNoteView.as_view(), name="get-archive"),
    path("archive/<int:note_id>/", ArchiveNoteView.as_view(), name="archive_note"),
    path("search/", SearchNoteView.as_view(), name="search"),
    path("filter/", FilterNotesView.as_view(), name="filter"),
]
