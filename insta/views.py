from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . forms import PostForm, UserProfileForm, CommentForm
from . models import Comment, Post, Profile

# Create your views here.

@login_required(login_url='accounts/login')
def editProfile(request, username):
    if username != request.user.username:
        return render(request, 'error.html')
    else:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                if Profile.objects.filter(editor__username = username).exists():
                    profile = Profile.objects.get(editor__username = username)
                    profile.profile_photo = form.cleaned_data['profile_photo']
                    profile.bio = form.cleaned_data['bio']
                    profile.editor = request.user
                    profile.save()
                else:
                    profile = form.save(commit=False)
                    profile.editor = request.user
                    profile.save()
        else:
            form = UserProfileForm()

        return render(request, 'profile.html', {"form": form})

def profile(request, username):
    checker = False
    if username == request.user.username:
        checker = True

    if Profile.objects.filter(editor__username = username).exists():
        profile = Profile.objects.filter(editor__username = username).first()
        if Post.objects.filter(editor__editor__username = username).exists():
            posts = Post.objects.filter(editor__username = username)
        else:
            posts = None
    else:
        profile = None
        posts = None
    return render(request, 'profile_d.html', {"profile": profile, "posts": posts, "checker": checker})
    