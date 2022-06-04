from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Profile(models.Model):
    profile_photo = CloudinaryField('image')
    bio = models.TextField(max_length=500)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
