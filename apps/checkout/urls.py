from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cart$', views.cart),
    url(r'^update-cart', views.update_cart),
    url(r'^confirm', views.confirm),
    url(r'^order-placed', views.processOrder),
]