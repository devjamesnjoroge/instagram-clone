from django.test import TestCase
from .models import Profile, Post, Comment, Like, Follow

# Create your tests here.
class ProfileTest(TestCase):
    def setUp(self):
        self.new_profile = Profile(profile_photo='image.jpg', bio='This is a bio', user='testuser')

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

    def test_get_profile_by_id(self):
        self.new_profile.create_profile()
        profiles = Profile.get_profile_by_id(1)
        self.assertTrue(profiles.id == 1)
