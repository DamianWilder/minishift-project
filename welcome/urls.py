from django.urls import path
from . import views

# url conf module
urlpatterns = [
    path("", views.index),
    path("index/", views.index),
    path("calculate/", views.calculate_chex),
]
