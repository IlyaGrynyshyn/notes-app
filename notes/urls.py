from django.urls import path
from .views import HomeView, DeleteNoteView, ArchiveNoteView, UnarchiveNoteView, CategoryView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("category/", CategoryView.as_view(), name='category' ),
    path('delete/<int:note_id>/', DeleteNoteView.as_view(), name='delete_note'),
    path('archive/<int:note_id>/', ArchiveNoteView.as_view(), name='archive_note'),
    path('unarchive/<int:note_id>/', UnarchiveNoteView.as_view(), name='unarchive_note'),
]
