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


class ExampleForm(forms.Form):
    """Simple example form used for demonstrating CSRF and validation."""

    name = forms.CharField(max_length=100)
    email = forms.EmailField()

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError('Name is required')
        return name
