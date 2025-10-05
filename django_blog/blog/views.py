from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import RegistrationForm, ProfileForm, PostForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Class-based views for Post CRUD
from django.urls import reverse_lazy
from django.views.generic import (
	ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home(request):
	return render(request, 'home.html')


def post_list(request):
	posts = Post.objects.all()
	return render(request, 'blog/post_list.html', {'posts': posts})


class PostListView(ListView):
	model = Post
	template_name = 'blog/post_list.html'
	context_object_name = 'posts'


class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'blog/post_confirm_delete.html'
	success_url = reverse_lazy('blog:post_list')

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user


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

