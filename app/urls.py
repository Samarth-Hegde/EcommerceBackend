from django.contrib import admin
from django.urls import include, path

from app.views import products

urlpatterns = [
    path("product/<int:product_id>/" , view=products.product),
    path("product/" , view=products.product)
]