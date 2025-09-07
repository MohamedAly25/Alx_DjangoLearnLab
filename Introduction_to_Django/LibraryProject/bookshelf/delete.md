# Delete Book

```python
from books_app.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
Expected Output
<QuerySet []>
