from django import forms
from .models import Profile, Post, Comment, Like, Follow

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['editor']
        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['editor']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'caption': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['editor', 'post']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        exclude = ['following', 'follow']