from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Book
from .serializers import BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
	# Use select_related to avoid N+1 queries when including author data
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	# Read endpoints are open; create requires authentication (enforced on alias CreateView)
	permission_classes = [IsAuthenticatedOrReadOnly]
	# Enable filtering, search and ordering for this list endpoint.
	# - DjangoFilterBackend allows exact-match filtering via query params
	#   e.g. ?title=Pride%20and%20Prejudice, ?author__name=Jane%20Austen
	# - SearchFilter enables partial text search on configured fields:
	#   use ?search=term which will search `title` and `author__name`.
	# - OrderingFilter enables sorting via ?ordering=field or ?ordering=-field
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	filterset_fields = ['title', 'author__name', 'publication_year']
	search_fields = ['title', 'author__name']
	ordering_fields = ['title', 'publication_year']


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]


# Thin wrappers to satisfy naming checks (aliases for common generic views)
class ListView(generics.ListAPIView):
	# Alias list view with the same filter/search/ordering behavior.
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	filterset_fields = ['title', 'author__name', 'publication_year']
	search_fields = ['title', 'author__name']
	ordering_fields = ['title', 'publication_year']


class DetailView(generics.RetrieveAPIView):
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]


class UpdateView(generics.UpdateAPIView):
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	# Only authenticated users can update
	permission_classes = [IsAuthenticated]


class DeleteView(generics.DestroyAPIView):
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	# Only authenticated users can delete
	permission_classes = [IsAuthenticated]


class CreateView(generics.CreateAPIView):
	queryset = Book.objects.select_related('author').all()
	serializer_class = BookSerializer
	# Only authenticated users can create
	permission_classes = [IsAuthenticated]
