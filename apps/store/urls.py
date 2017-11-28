from django.conf.urls import url
from . import views

urlpatterns = [
    # pages
    url(r'^$', views.index),
    url(r'^results$', views.results),
    url(r'^game/(?P<num>[0-9]+)$', views.game),
    url(r'^user/(?P<user_id>\d+)$', views.user), 

    # functions
    url(r'^add_to_cart', views.add_to_cart),
    url(r'^results_process', views.results_process),
    url(r'^view_all', views.view_all),

]