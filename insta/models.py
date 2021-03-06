from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class Profile(models.Model):
    profile_photo = CloudinaryField('image')
    bio = HTMLField()
    editor = models.OneToOneField(User, on_delete=models.CASCADE)

    def create_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()
        return profile

    @classmethod
    def get_profile_by_id(cls, id):
        profile = Profile.objects.get(id=id)
        return profile

    def __str__(self):
        return self.editor.username

class Post(models.Model):
    image = CloudinaryField('image')
    caption = models.TextField(max_length=500)
    editor = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    @classmethod
    def get_post(cls):
        post = Post.objects.all()
        return post

    @classmethod
    def get_post_by_id(cls, id):
        post = Post.objects.get(id=id)
        return post


class Comment(models.Model):
    comment = models.TextField(max_length=500)
    editor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()


class Like(models.Model):
    editor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def save_like(self):
        self.save()

    def delete_like(self):
        self.delete()

class Follow(models.Model):
    following = models.ForeignKey(Profile, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
