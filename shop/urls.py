from django.urls import path

from . import views

urlpatterns = [
    path('catalog', views.catalogue, name='catalogue'),
    path('subcategory/<int:id>', views.subcategory, name='subcategory'),
    path('search', views.search, name='search'),
    path('contacts', views.contacts, name='contacts'),
    path('about', views.about, name='about'),
    path('order', views.order, name='order'),
    path('', views.index, name='index'),
]
