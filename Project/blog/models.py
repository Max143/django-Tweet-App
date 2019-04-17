from django.db import models
from django.utils import timezone  # for importing timezone into consideration
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)   #@ timezone.now() is function which we are not using here
	author = models.ForeignKey(User, on_delete=models.CASCADE)	

	#  auto_now_add=True --> update date and time only when object created
	#  auto_now=True -- >  it means that it will update the date time every time the post is updated)

	def __str__(self):
		return self.title  

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})


# python manage.py sqlmigrate blog  will show all the sql code in terminal 