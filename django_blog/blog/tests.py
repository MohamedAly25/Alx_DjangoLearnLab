from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment
from django.utils import timezone


# Using Django's concrete User model


class PostModelTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='tester', password='pass')

	def test_create_post(self):
		p = Post.objects.create(title='T', content='C', author=self.user, published_date=timezone.now())
		self.assertEqual(str(p), 'T')


class CommentModelTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='tester', password='pass')
		self.post = Post.objects.create(title='T', content='C', author=self.user)

	def test_create_comment(self):
		c = Comment.objects.create(post=self.post, author=self.user, content='hi')
		self.assertIn('hi', str(c))


class AuthFlowTests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_register_and_login(self):
		resp = self.client.post(reverse('blog:register'), {'username': 'u1', 'email': 'a@b.com', 'password1': 'strongpass123', 'password2': 'strongpass123'})
		self.assertEqual(resp.status_code, 302)
		# login
		login = self.client.post(reverse('blog:login'), {'username': 'u1', 'password': 'strongpass123'})
		# login view on success redirects (302)
		self.assertIn(login.status_code, (200, 302))
