from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from notes.forms import NoteForm, CategoryForm
from notes.models import Note, Category
from django.views.generic import ListView, DeleteView


class FilterNotesView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "filter_node.html"
    context_object_name = "notes"
    ordering = "-created_at"

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user, archived=False)
        category = self.request.GET.get("category")
        if category and category != "all":
            queryset = queryset.filter(category__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(user=self.request.user)
        return context


class CategoryListView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        category_name = request.POST.get("name")
        color = request.POST.get("color")
        Category.objects.create(user=request.user, name=category_name, color=color)
        return redirect("notes-list")


class CategoryUpdateView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(instance=category)
        return render(
            request, "category_edit.html", {"form": form, "category": category}
        )

    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("notes-list")
        return render(
            request, "category_edit.html", {"form": form, "category": category}
        )


class CategoryDeleteView(LoginRequiredMixin, View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return redirect("notes-list")


class NotesListView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = Note.objects.filter(user=request.user).filter(archived=False)
        categories = Category.objects.filter(user=request.user)
        return render(
            request, "home.html", {"notes": queryset, "categories": categories}
        )

    def post(self, request):
        text = request.POST.get("text")
        category_name = request.POST.get("category")
        category, created = Category.objects.get_or_create(name=category_name)
        Note.objects.create(user=request.user, text=text, category=category)
        return redirect("notes-list")


class NoteUpdateView(LoginRequiredMixin, View):
    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id, user=request.user)
        form = NoteForm(instance=note)
        return render(request, "note_edit.html", {"form": form, "note": note})

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id, user=request.user)
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("notes-list")
        return render(request, "note_edit.html", {"form": form, "note": note})


class NoteDeleteView(LoginRequiredMixin, View):
    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        note.delete()
        return redirect("notes-list")


class ArchiveNoteView(LoginRequiredMixin, View):
    def get(self, request):
        notes = (
            Note.objects.filter(user=request.user)
            .filter(archived=True)
            .order_by("-created_at")
        )
        categories = Category.objects.filter(user=request.user)
        context = {"notes": notes, "categories": categories}
        return render(request, "archive.html", context)

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        note.archived = not note.archived
        note.save()
        return redirect("notes-list")


class SearchNoteView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("query")
        notes = (
            Note.objects.filter(user=request.user)
            .filter(archived=False)
            .filter(text__contains=query)
            .order_by("-created_at")
        )
        categories = Category.objects.filter(user=request.user)
        context = {"notes": notes, "categories": categories}
        return render(request, "archive.html", context)
