from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def home(request):
	return render(request, 'home.html')


def post_list(request):
	posts = Post.objects.all()
	return render(request, 'blog/post_list.html', {'posts': posts})


def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('blog:home')
	else:
		form = RegistrationForm()
	return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('blog:profile')
	else:
		form = ProfileForm(instance=request.user)
	return render(request, 'registration/profile.html', {'form': form})

