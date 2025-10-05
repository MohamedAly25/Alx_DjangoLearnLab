from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date']
        widgets = {
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
