from django.urls import path
from . import views

urlpatterns = [
    path("users/<int:id>/",view=views.user),
    path("users/",view=views.user)
]