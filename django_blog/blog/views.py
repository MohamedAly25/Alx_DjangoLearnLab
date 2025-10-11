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
from .forms import CommentForm
from .models import Comment
from django.views import View
from taggit.models import Tag



def home(request):
	return render(request, 'home.html')


def post_list(request):
	posts = Post.objects.all()
	return render(request, 'blog/post_list.html', {'posts': posts})


class PostListView(ListView):
	model = Post
	template_name = 'post_list.html'
	context_object_name = 'posts'


class PostDetailView(DetailView):
	model = Post
	template_name = 'post_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comment_form'] = CommentForm()
		return context


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		response = super().form_valid(form)
		tags = form.cleaned_data.get('tags')
		if tags:
			tag_list = [t.strip() for t in tags.split(',') if t.strip()]
			# TaggableManager.set expects an iterable of tag names/objects
			self.object.tags.set(tag_list)
		return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = 'post_form.html'

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user
    
	def form_valid(self, form):
		response = super().form_valid(form)
		tags = form.cleaned_data.get('tags')
		if tags is not None:
			tag_list = [t.strip() for t in tags.split(',') if t.strip()]
			# TaggableManager.set expects an iterable of tag names/objects
			self.object.tags.set(tag_list)
		return response


def posts_by_tag(request, tag_name):
	posts = Post.objects.filter(tags__name__in=[tag_name])
	return render(request, 'tag_list.html', {'posts': posts, 'tag': tag_name})


class PostByTagListView(ListView):
	model = Post
	template_name = 'tag_list.html'
	context_object_name = 'posts'

	def get_queryset(self):
		slug = self.kwargs.get('tag_slug')
		return (
			Post.objects.select_related('author')
			.prefetch_related('tags')
			.filter(tags__slug=slug)
			.distinct()
			.order_by('-published_date')
		)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs.get('tag_slug')
		try:
			tag = Tag.objects.get(slug=slug)
			context['tag'] = tag.name
		except Tag.DoesNotExist:
			context['tag'] = slug
		return context


def search(request):
    """Search for posts by title, content, author, or tags."""
    q = request.GET.get('q', '').strip()
    results = Post.objects.none()
    if q:
        # Move import to top of file in production
        from django.db.models import Q
        results = (
            Post.objects.select_related('author')
            .prefetch_related('tags')
            .filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q) |
                Q(author__username__icontains=q)
            )
            .distinct()
            .order_by('-published_date')
        )
    return render(
        request,
        'search_results.html',
        {
            'results': results,
            'query': q,
            'total_count': results.count() if q else 0,
        }
    )


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'post_confirm_delete.html'
	success_url = reverse_lazy('blog:blog-home')

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user


class CommentCreateView(LoginRequiredMixin, View):
	def post(self, request, pk):
		post = get_object_or_404(Post, pk=pk)
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = request.user
			comment.post = post
			comment.save()
		# After creating (or failing validation), redirect back to the post detail
		return redirect('blog:post-detail', pk=pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Comment
	form_class = CommentForm
	template_name = 'comment_form.html'

	def get_success_url(self):
		return reverse_lazy('blog:post-detail', kwargs={'pk': self.object.post.pk})

	def test_func(self):
		comment = self.get_object()
		return comment.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = 'comment_confirm_delete.html'

	def get_success_url(self):
		return reverse_lazy('blog:post-detail', kwargs={'pk': self.object.post.pk})

	def test_func(self):
		comment = self.get_object()
		return comment.author == self.request.user


def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('blog:blog-home')
	else:
		form = RegistrationForm()
	return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('blog:profile')
	else:
		form = ProfileForm(instance=request.user)
	return render(request, 'profile.html', {'form': form})

