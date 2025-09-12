from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Books
    path('books/', views.list_books, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),

    # Library detail
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Roles
    path("role/admin/", views.admin_view, name="admin_view"),
    path("role/librarian/", views.librarian_view, name="librarian_view"),
    path("role/member/", views.member_view, name="member_view"),
]
