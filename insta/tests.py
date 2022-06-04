from django.test import TestCase
from . models import Profile, Post, Comment, Like, Follow
from django.contrib.auth.models import User

# Create your tests here.

class ProfileTest(TestCase):
    def setUp(self):
        user=User.objects.get_or_create(username='test_user')[0]
        self.new_profile = Profile(profile_photo='image.jpg', bio='This is a bio', user=user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile, Profile))

    def test_save_profile(self):
        self.new_profile.create_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete_profile(self):
        self.new_profile.create_profile()
        self.new_profile.delete_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) == 0)

    def test_get_profile(self):
        self.new_profile.create_profile()
        profiles = Profile.get_profile()
        self.assertTrue(len(profiles) > 0)


class PostTest(TestCase):
    def setUp(self):
        user=User.objects.get_or_create(username='test_user')[0]       
        self.new_post = Post(image='image.jpg', caption='This is a caption', user=user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post, Post))

    def test_save_post(self):
        self.new_post.save_post()
        posts = Post.objects.all()
        self.assertTrue(len(posts) > 0)

    def test_delete_post(self):
        self.new_post.save_post()
        self.new_post.delete_post()
        posts = Post.objects.all()
        self.assertTrue(len(posts) == 0)

    def test_get_post(self):
        self.new_post.save_post()
        posts = Post.get_post()
        self.assertTrue(len(posts) > 0)

class CommentTest(TestCase):
    def setUp(self):
        user=User.objects.get_or_create(username='test_user')[0]
        post = Post.objects.get_or_create(image='image.jpg', caption='This is a caption', user=user)[0]
        self.new_comment = Comment(comment='This is a comment',post=post, user=user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))

    def test_save_comment(self):
        self.new_comment.save_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments) > 0)

    def test_delete_comment(self):
        self.new_comment.save_comment()
        self.new_comment.delete_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments) == 0) 

class LikeTest(TestCase):
    def setUp(self):
        user=User.objects.get_or_create(username='test_user')[0]
        post = Post.objects.get_or_create(image='image.jpg', caption='This is a caption', user=user)[0]
        self.new_like = Like(user=user, post=post)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_like, Like))

    def test_save_like(self):
        self.new_like.save_like()
        likes = Like.objects.all()
        self.assertTrue(len(likes) > 0)

    def test_delete_like(self):
        self.new_like.save_like()
        self.new_like.delete_like()
        likes = Like.objects.all()
        self.assertTrue(len(likes) == 0)

