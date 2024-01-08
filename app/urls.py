from django.contrib import admin
from django.urls import include, path

from app.views import products,cart

urlpatterns = [
    path("product/<int:product_id>/" , view=products.product),
    path("product/" , view=products.product),
    path("cart/add/", view = cart.add_to_cart),
    path("cart/clear/", view = cart.clear_cart)
]