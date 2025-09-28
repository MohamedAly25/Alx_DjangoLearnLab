# advanced-api-project

This is a small Django REST Framework project exposing a `Book` API with filtering, searching, and ordering support.

Endpoints (prefixed with `/api/`):

- `GET /api/books/` - list books (supports filtering, search, ordering)
- `POST /api/books/` - create a book (authenticated users)
- `GET /api/books/<id>/` - retrieve book
- `PUT /api/books/<id>/` - update book (authenticated users)
- `DELETE /api/books/<id>/` - delete book (authenticated users)

Filtering, searching, and ordering
---------------------------------

The list endpoint supports the following query params:

- Filtering by exact fields using query params, e.g.:
  - `?title=Pride%20and%20Prejudice`
  - `?author__name=Jane%20Austen`
  - `?publication_year=1813`
- Searching (partial, case-insensitive) using `search`:
  - `?search=Jane` will look for books whose title or author's name contains "Jane".
- Ordering using `ordering` (prefix with `-` for descending):
  - `?ordering=title`
  - `?ordering=-publication_year`

Examples (curl):

```
# List books filtered by title
curl "http://localhost:8000/api/books/?title=Pride%20and%20Prejudice"

# Search by author name
curl "http://localhost:8000/api/books/?search=Jane"

# Order by publication year descending
curl "http://localhost:8000/api/books/?ordering=-publication_year"
```

Running tests
-------------

Run the test suite for the `api` app:

```
python manage.py test api
```
