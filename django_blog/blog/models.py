from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	published_date = models.DateTimeField(null=True, blank=True)
	author = models.ForeignKey(
		get_user_model(), on_delete=models.CASCADE, related_name='posts'
	)

	class Meta:
		ordering = ['-published_date']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={'pk': self.pk})

	# tags
	tags = TaggableManager(blank=True)


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_at']

	def __str__(self):
		# include a short excerpt of the comment content for readability
		excerpt = (self.content[:47] + '...') if len(self.content) > 50 else self.content
		return f'Comment by {self.author} on {self.post}: {excerpt}'
