from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
	books = Book.objects.all()
	return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_create(request):
	if request.method == 'POST':
		form = BookForm(request.POST)
		if form.is_valid():
			form.save()
			return render(request, 'bookshelf/book_list.html', {'books': Book.objects.all()})
	else:
		form = BookForm()
	return render(request, 'bookshelf/form_example.html', {'form': form})


@permission_required('bookshelf.can_edit', raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_edit(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == 'POST':
		form = BookForm(request.POST, instance=book)
		if form.is_valid():
			form.save()
			return render(request, 'bookshelf/book_list.html', {'books': Book.objects.all()})
	else:
		form = BookForm(instance=book)
	return render(request, 'bookshelf/form_example.html', {'form': form})
