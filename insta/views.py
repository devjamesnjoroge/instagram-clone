from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . forms import PostForm, UserProfileForm, CommentForm
from . models import Comment, Post, Profile

# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    posts = Post.objects.all()
    pfile = Profile()
    user = request.user
    if Profile.objects.filter(editor=request.user).exists():
        profile = Profile.objects.get(editor=user)
        profile_photo = profile.profile_photo
    else:
        profile = None
        profile_photo = None
    return render(request, 'index.html', {"posts": posts, "profile_photo": profile_photo, "profile": profile, "pfile": pfile})

@login_required(login_url='/accounts/login/')
def profile(request, uname):
    if Profile.objects.filter(editor=request.user).exists():
       profile = Profile.objects.get(editor=request.user)
       profile_display = Profile.objects.get(editor__username=uname)
    else:
        profile = None
        profile_display = None
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
    return render(request, 'profile.html', {"form": form, "profile": profile, "profile_display": profile_display})

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

def comment(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(id=id)
            comment = form.save(commit=False)
            comment.editor = request.user
            comment.post = post
            comment.save()
    else:
        form = CommentForm()
    return render(request, 'comments.html', {"form": form, "comments": comments})