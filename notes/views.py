from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from notes.models import Note, Category
from django.views.generic import ListView


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return

    def post(self, request, *args, **kwargs):
        category_name = request.POST.get('name')
        color = request.POST.get('color')
        Category.objects.create(user=request.user, name=category_name, color=color)
        return redirect('home')


class HomeView(View):
    def get(self, request):
        queryset = Note.objects.filter(user=request.user).filter(archived=False)

        sort_by = request.GET.get('sort_by')
        if sort_by == 'date':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'word_count':
            queryset = sorted(queryset, key=lambda x: len(x.text.split()), reverse=True)
        elif sort_by == 'unique_words':
            queryset = sorted(queryset, key=lambda x: len(set(x.text.split())), reverse=True)

        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)

        # notes = Note.objects.filter(user=request.user).order_by("-created_at").filter(
        #     Q(category__in=self.request.GET.getlist('category'))
        # )

        categories = Category.objects.filter(user=request.user)
        return render(request, 'home.html', {'notes': queryset, 'categories': categories})

    def post(self, request):
        text = request.POST.get('text')
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        Note.objects.create(user=request.user, text=text, category=category)
        return redirect('home')


class DeleteNoteView(View):
    def post(self, request, note_id):
        note = Note.objects.get(id=note_id)
        note.delete()
        return redirect('home')


class ArchiveNoteView(View):
    def get(self, request):
        notes = Note.objects.filter(user=request.user).filter(archived=True).order_by('-created_at')
        categories = Category.objects.filter(user=request.user)
        context = {'notes': notes, 'categories': categories}
        return render(request, "archive.html", context)

    def post(self, request, note_id):
        note = Note.objects.get(id=note_id)
        note.archived = not note.archived
        note.save()
        return redirect('home')


class SearchNoteView(View):
    def get(self, request):
        query = request.GET.get('query')
        notes = Note.objects.filter(user=request.user).filter(archived=False).filter(text__contains=query).order_by('-created_at')
        categories = Category.objects.filter(user=request.user)
        context = {'notes': notes, 'categories': categories}
        return render(request, 'archive.html', context)

class FilterMovieView(View):
    def get_queryset(self):
        queryset = Note.objects.filter(
            Q(category__in=self.request.GET.getlist['category'])
        )
        return queryset