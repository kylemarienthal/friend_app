from django.conf.urls import url, include
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.all_friends, name='dashboard'),
    url(r'^user/(?P<id>\d+)$', views.user_profile, name = 'user_profile'),
    url(r'^add/(?P<id>\d+)$', views.add_friend, name = 'add_friend'),
    url(r'^remove/(?P<id>\d+)$', views.remove_friend, name = 'remove_friend')
]
