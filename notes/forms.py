from django import forms
from notes.models import Note, Category

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text', 'category']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
        }
