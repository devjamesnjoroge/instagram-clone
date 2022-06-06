from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from . forms import PostForm, UserProfileForm, CommentForm, FollowForm
from . models import Comment, Follow, Post, Profile, Like
from django.http import HttpResponseRedirect

# Create your views here.

@login_required(login_url='accounts/login')
def like(request, id):

    if Like.objects.filter(editor__editor = request.user, post__id = id).exists():
        if request.method == 'POST':
            like_object = Like.objects.get(editor__editor = request.user, post__id = id)
            like_object.delete()
            return redirect('/')


    else:
        if request.method == 'POST':
            like = Like()
            like.post = Post.objects.get(id = id)
            like.editor = Profile.objects.get(editor = request.user)
            like.save()
            return redirect('/')


    return redirect('/')



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
    posts = Post.objects.all()
    return render(request, 'index.html', {"posts": posts, "profile": profile, 'color': 'red'})

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
                    return HttpResponseRedirect(request.path_info)
                else:
                    profile = form.save(commit=False)
                    profile.editor = request.user
                    profile.save()
                    return HttpResponseRedirect(request.path_info)
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

    if Follow.objects.filter(following__editor__username = username, follower_id = request.user.id):
        is_following = True
        text = 'Unfollow'
        if request.method == 'POST':
            follow_object = Follow.objects.get(following__editor__username = username, follower_id = request.user.id)
            follow_object.delete()
            return HttpResponseRedirect(request.path_info)

    else:
        text = 'Follow'
        if request.method == 'POST':
            follow = Follow()
            follow.following = Profile.objects.get(editor__username = username)
            follow.follower = request.user
            follow.save()
            return HttpResponseRedirect(request.path_info)
    following = Follow.objects.filter(follower__username = username).all()
    followers = Follow.objects.filter(following__editor__username = username)
    following_count = following.count()
    followers_count= followers.count()
    return render(request, 'profile_d.html', {"profile": profile, "posts": posts, "checker": checker, 'text': text, 'f_count': following_count, 'fr_count': followers_count})

@login_required(login_url='accounts/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.editor = request.user.profile
            post.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'post.html', {"form": form})


@login_required(login_url='accounts/login')
def comment(request, id):
    if Comment.objects.filter(post__id = id).exists():
        comments = Comment.objects.filter(post__id = id)
    else:
        comments = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(id=id)
            comment.editor = request.user.profile
            comment.save()
            return HttpResponseRedirect(request.path_info)
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

