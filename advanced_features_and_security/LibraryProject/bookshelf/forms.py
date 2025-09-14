from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        # Basic validation: strip and limit length
        title = title.strip()
        if not title:
            raise forms.ValidationError('Title cannot be empty')
        return title
