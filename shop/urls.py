from django.urls import path

from . import views

urlpatterns = [
    path('catalog', views.catalogue, name='catalogue'),
    path('subcategory/<int:id>', views.subcategory, name='subcategory'),
    path('search', views.search, name='search'),
    path('', views.index, name='index'),
]
