from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^searchProducts', views.searchProducts),
    url(r'^orders', views.orders),
    url(r'^orderSearch', views.orderSearch),
    url(r'^add-product', views.addProduct),
    url(r'^select-game/(?P<game_id>[0-9]+)', views.select_game),
    url(r'create-game', views.create_game),
    url(r'^edit-game/(?P<game_id>[0-9]+)', views.edit_game),
    url(r'^edit-order/(?P<order_id>[0-9]+)', views.edit_order),
    url(r'^update-game', views.update_game), 
    url(r'^update-order', views.update_order),
]