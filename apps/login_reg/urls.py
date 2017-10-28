from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/(?P<page_id>[0-9]+)', views.sign_in),
    url(r'^/register', views.register),
    url(r'^/login', views.login),
    url(r'^/logout', views.logout),
    url(r'^/', views.sign_in),
]