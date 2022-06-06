from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    path('<username>/edit', views.editProfile, name='profile'),
    path('<username>', views.profile, name='profile'),
    # url(r'^post/$', views.post, name='post'),
    # path('comment/<int:id>', views.comment, name='comment'),
]