from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^results', views.results),
    url(r'^game/(?P<num>\d)$', views.game)
]