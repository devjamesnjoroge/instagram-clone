from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . forms import PostForm, UserProfileForm
from . models import Post, Profile

# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {"posts": posts})

@login_required(login_url='/accounts/login/')
def profile(request):
    if Profile.objects.filter(editor=request.user).exists():
       profile = Profile.objects.get(editor=request.user)
    else:
        profile = None
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if Profile.objects.filter(editor=request.user).exists():
                profile = Profile.objects.get(editor=request.user)
                profile.profile_photo = form.cleaned_data['profile_photo']
                profile.bio = form.cleaned_data['bio']
                profile.save()
            else:
                profile = form.save(commit=False)
                profile.editor = request.user
                form.save()
    else:
        form = UserProfileForm()
    return render(request, 'profile.html', {"form": form, "profile": profile})

def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.editor = request.user
            post.save()
    else:
        form = PostForm()
    return render(request, 'post.html', {"form": form})