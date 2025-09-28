from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
import datetime


class BookViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for authentication when needed
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(username='tester', password='pass')
        # Resolve models via the app registry to avoid import-time issues
        from django.apps import apps
        self.Author = apps.get_model('api', 'Author')
        self.Book = apps.get_model('api', 'Book')

        # Create authors and books
        self.author = self.Author.objects.create(name='Jane Austen')
        self.book = self.Book.objects.create(
            title='Pride and Prejudice', publication_year=1813, author=self.author
        )
        # second book for filtering/searching
        self.book2 = self.Book.objects.create(
            title='Sense and Sensibility', publication_year=1811, author=self.author
        )

    def test_list_books_returns_200_and_expected_fields(self):
        url = reverse('book-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, list)
        # Check keys in first item
        first = resp.data[0]
        self.assertIn('id', first)
        self.assertIn('title', first)
        self.assertIn('publication_year', first)
        self.assertIn('author', first)

    def test_retrieve_book_returns_200_and_correct_data(self):
        url = reverse('book-detail', args=[self.book.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.data
        self.assertEqual(data['title'], 'Pride and Prejudice')
        self.assertEqual(data['publication_year'], 1813)
        self.assertEqual(data['author'], self.author.id)

    def test_create_book_authenticated_returns_201_and_saves(self):
        self.client.login(username='tester', password='pass')
        url = reverse('book-list')
        payload = {'title': 'New Book', 'publication_year': 2020, 'author': self.author.id}
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.Book.objects.filter(title='New Book').exists())

    def test_create_book_unauthenticated_is_forbidden(self):
        url = reverse('book-list')
        payload = {'title': 'NoAuth Book', 'publication_year': 2020, 'author': self.author.id}
        resp = self.client.post(url, payload, format='json')
        # Unauthenticated clients should receive 401 for endpoints requiring auth to create
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated_updates(self):
        self.client.login(username='tester', password='pass')
        url = reverse('book-detail', args=[self.book.id])
        payload = {'title': 'Pride & Prejudice', 'publication_year': 1813, 'author': self.author.id}
        resp = self.client.put(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Pride & Prejudice')

    def test_delete_book_authenticated_deletes(self):
        self.client.login(username='tester', password='pass')
        url = reverse('book-detail', args=[self.book2.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.Book.objects.filter(id=self.book2.id).exists())

    def test_publication_year_future_validation_returns_400(self):
        self.client.login(username='tester', password='pass')
        url = reverse('book-list')
        next_year = datetime.date.today().year + 1
        payload = {'title': 'Future Book', 'publication_year': next_year, 'author': self.author.id}
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', resp.data)

    def test_filter_search_order_behave_expected(self):
        url = reverse('book-list')
        # Filter by title
        resp = self.client.get(url, {'title': 'Pride and Prejudice'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

        # Search by author name
        resp = self.client.get(url, {'search': 'Jane'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 2)

        # Order by publication_year desc
        resp = self.client.get(url, {'ordering': '-publication_year'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b['publication_year'] for b in resp.data]
        self.assertEqual(years, sorted(years, reverse=True))
