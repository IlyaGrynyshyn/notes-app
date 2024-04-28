from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from notes.models import Note, Category, CategoryColor
from django.views.generic import ListView


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


class CategoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(user=request.user)
        context = {"categories": categories}
        return JsonResponse(context)

    def post(self, request, *args, **kwargs):
        category_name = request.POST.get("name")
        color = request.POST.get("color")
        category_color = CategoryColor.objects.create(color_code=color)
        Category.objects.create(
            user=request.user, name=category_name, color=category_color
        )
        return redirect("home")


class HomeView(LoginRequiredMixin, View):
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
        return redirect("home")


class DeleteNoteView(LoginRequiredMixin, View):
    def post(self, request, note_id):
        note = Note.objects.get(id=note_id)
        note.delete()
        return redirect("home")


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
        return redirect("home")


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
