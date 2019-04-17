from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=199, blank=True)
	location = models.CharField(max_length=99, blank=True)
	image = models.ImageField(default='profile.jpg', upload_to='profile_pics')
	
	def __str__(self):
		return f'{ self.user.username }  Profile'

	

	



	

