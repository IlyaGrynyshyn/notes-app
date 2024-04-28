from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100, db_index=True, unique=True)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Note(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, db_index=True, related_name='note')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    archived = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"Note by {self.user.username} - {self.created_at}"

    @property
    def word_count(self):
        return len(self.text.split())

    class Meta:
        ordering = ['-created_at']
