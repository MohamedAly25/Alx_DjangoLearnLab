"""
API models for the example project.

Models:
 - Author: simple author record with a name
 - Book: represents a book with title, publication_year and a ForeignKey to Author

The Book.author FK uses related_name='books' so that Author instances can access
their books via `author.books.all()`.
"""
from django.db import models


class Author(models.Model):
	"""An author of one or more books.

	Fields:
	- name: full name of the author
	"""

	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name


class Book(models.Model):
	"""A book entry.

	Fields:
	- title: title of the book
	- publication_year: year the book was published
	- author: ForeignKey to Author with related_name='books'

	Using related_name='books' makes Author.books available for nesting in serializers.
	"""

	title = models.CharField(max_length=512)
	publication_year = models.IntegerField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

	def __str__(self):
		return f"{self.title} ({self.publication_year})"

