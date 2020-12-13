from django.urls import path

from . import views

urlpatterns = [
    path('catalog', views.catalogue, name='catalogue'),
    path('', views.index, name='index'),
]
