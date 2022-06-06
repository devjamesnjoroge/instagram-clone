from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('<username>/edit', views.editProfile, name='profile'),
    path('<username>', views.profile, name='profile'),
    url(r'^post/$', views.create_post, name='post'),
    path('comment/<int:id>', views.comment, name='comment'),
    path('profile/search', views.search, name='search'),
    path('like/<int:id>', views.like, name='like')
]