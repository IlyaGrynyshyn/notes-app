import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class CategoryColor(models.Model):
    color_code = models.CharField(max_length=50)

    def __str__(self):
        return self.color_code

    def clean(self):
        color_code_pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
        if not re.match(color_code_pattern, self.color_code):
            raise ValidationError(
                "The color code format is incorrect. Use the #RRGGBB or #RGB format."
            )


class Category(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100, db_index=True, unique=True)
    color = models.ForeignKey(CategoryColor, on_delete=models.DO_NOTHING, db_index=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="note",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    archived = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"Note by {self.user.username} - {self.created_at}"

    class Meta:
        ordering = ["-created_at"]
