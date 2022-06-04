from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . forms import UserProfileForm

# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm()
    return render(request, 'index.html', {"form": form})