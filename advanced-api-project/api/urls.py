from django.urls import path
from .views import (
	BookListCreateView,
	BookRetrieveUpdateDestroyView,
	CreateView,
	UpdateView,
	DeleteView,
)

urlpatterns = [
	path('books/', BookListCreateView.as_view(), name='book-list'),
	path('books/create', CreateView.as_view(), name='book-create'),
	path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
	path('books/update/<int:pk>/', UpdateView.as_view(), name='book-update'),
	path('books/delete/<int:pk>/', DeleteView.as_view(), name='book-delete'),
]
