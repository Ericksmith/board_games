from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^searchProducts', views.searchProducts),
    url(r'^add-product', views.addProduct),
    url(r'^select-game/(?P<game_id>[0-9]+)', views.select_game),
    url(r'create-game', views.create_game),
]