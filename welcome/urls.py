from django.conf.urls import include, url
from . import views

# url conf module
urlpatterns = [
    url(r'^$', views.index),
    url(r"^index/", views.index),
    url(r"^calculate/", views.calculate_chex),
]
