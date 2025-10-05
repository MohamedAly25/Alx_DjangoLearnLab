from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date']
        widgets = {
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # optional tags input (comma separated)
    tags = forms.CharField(required=False, help_text='Comma-separated tags', label='Tags')

    def __init__(self, *args, **kwargs):
        # if editing an instance, pre-fill tags field
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance and hasattr(instance, 'tags'):
            try:
                tag_names = instance.tags.names()
                self.fields['tags'].initial = ', '.join(tag_names)
            except Exception:
                # taggit may not be installed in some environments during static analysis
                self.fields['tags'].initial = ''



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'rows': 3})}
