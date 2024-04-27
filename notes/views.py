from django.shortcuts import render, redirect
from django.views import View
from notes.models import Note, Category

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return

    def post(self, request, *args, **kwargs):
        category_name = request.POST.get('category')
        color = request.POST.get('color')
        print(color)
        print("I am")
        Category.objects.get_or_create(name=category_name, color=color)
        return redirect('home')



class HomeView(View):
    def get(self, request):
        notes = Note.objects.all()
        categories = Category.objects.all()
        return render(request, 'home.html', {'notes': notes, 'categories': categories})

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
    def post(self, request, note_id):
        note = Note.objects.get(id=note_id)
        note.archived = True
        note.save()
        return redirect('home')

class UnarchiveNoteView(View):
    def post(self, request, note_id):
        note = Note.objects.get(id=note_id)
        note.archived = False
        note.save()
        return redirect('home')
