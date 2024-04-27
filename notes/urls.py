from django.urls import path
from .views import HomeView, DeleteNoteView, ArchiveNoteView, CategoryView, SearchNoteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("category/", CategoryView.as_view(), name='category' ),
    path('delete/<int:note_id>/', DeleteNoteView.as_view(), name='delete_note'),
    path('archive/', ArchiveNoteView.as_view(), name='get-archive'),
    path('archive/<int:note_id>/', ArchiveNoteView.as_view(), name='archive_note'),
    path("search/", SearchNoteView.as_view(), name='search')
]
