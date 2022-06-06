from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . forms import PostForm, UserProfileForm, CommentForm
from . models import Comment, Post, Profile

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    if Profile.objects.filter(editor=request.user).exists():
        profile = Profile.objects.get(editor=request.user)
    else:
        profile = None
    if Post.objects.filter(editor__editor__username = request.user.username).exists():
        posts = Post.objects.filter(editor__editor__username = request.user.username)
    else:
        posts = None
    return render(request, 'index.html', {"posts": posts, "profile": profile})

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

@login_required(login_url='accounts/login')
def profile(request, username):
    checker = False
    if username == request.user.username:
        checker = True

    if Profile.objects.filter(editor__username = username).exists():
        profile = Profile.objects.filter(editor__username = username).first()
        if Post.objects.filter(editor__editor__username = username).exists():
            posts = Post.objects.filter(editor__editor__username = username)
        else:
            posts = None
    else:
        profile = None
        posts = None
    return render(request, 'profile_d.html', {"profile": profile, "posts": posts, "checker": checker})

@login_required(login_url='accounts/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.editor = request.user.profile
            post.save()
    else:
        form = PostForm()
    return render(request, 'post.html', {"form": form})


@login_required(login_url='accounts/login')
def comment(request, id):
    if Comment.objects.all().exists():
        comments = Comment.objects.all()
    else:
        comments = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(id=id)
            comment.editor = request.user.profile
            comment.save()
    else:
        form = CommentForm()
    return render(request, 'comments.html', {"form": form, "comments": comments})


@login_required(login_url='accounts/login')
def search(request):
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        profiles = Profile.objects.filter(editor__username__icontains=search_term).all()
        return render(request, 'search.html', {"profiles": profiles})
    else:
        return render(request, 'search.html')