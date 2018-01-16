from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status = 'published')

class Post(models.Model):
	STATUS_CHANGES = (
		('draft', 'Roboczy'),
		('published', 'Opublikowany'),
		)
	title = models.CharField(max_length = 250)
	slug = models.SlugField(max_length = 250, unique_for_date = 'publish')
	author = models.ForeignKey(User, related_name = 'blog_posts', on_delete = models.CASCADE)#parametr z kaskadą ważny w WIN10
	body = models.TextField()
	publish = models.DateTimeField(default = timezone.now)
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	status = models.CharField(max_length = 10, choices = STATUS_CHANGES, default = 'draft')
	objects = models.Manager() #standard menager
	published = PublishedManager() #non-standard menager dunno what it does yet

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_abs_url(self):
		return reverse('blog:post_detail', args = [
			self.publish.year,
			self.publish.strftime('%m'),
			self.publish.strftime('%d'),
			self.slug
			])