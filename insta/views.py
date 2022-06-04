from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . forms import UserProfileForm
from . models import Profile

# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    if Profile.objects.filter(editor=request.user).exists():
       profile = Profile.objects.get(editor=request.user)
    else:
        profile = None
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.editor = request.user
            form.save()
    else:
        form = UserProfileForm()
    return render(request, 'index.html', {"form": form, "profile": profile})
