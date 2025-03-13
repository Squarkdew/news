from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
           'title',
           'content',
           'categories'
           
        ]

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 20:
            raise ValidationError("Описание должно содержать минимум 20 символов.")
        return content
  