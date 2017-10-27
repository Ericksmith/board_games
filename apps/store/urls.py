from django.conf.urls import url
from . import views

urlpatterns = [
    # pages
    url(r'^$', views.index),
    url(r'^results', views.results),
    url(r'^game/(?P<num>\d)$', views.game),

    # functions
    url(r'^add_to_cart', views.add_to_cart),

]