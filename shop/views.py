from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from shop.models import Item, Category, Subcategory
import random
from collections import OrderedDict

from .forms import SearchForm

def index(request):
    newItems = list(Item.objects.filter(new=True))
    showcase = random.sample(newItems, 3)
    template = loader.get_template('shop/index.html')
    context = {
        'showcase': showcase,
    }
    return HttpResponse(template.render(context, request))

def catalogue(request):
    links = OrderedDict()
    categories = list(Category.objects.all())
    for i in categories:
        subcategories = Subcategory.objects.filter(parent__id=i.id)
        links[i] = list(subcategories)
    template = loader.get_template('shop/assort.html')
    form = SearchForm()
    context = {
        'links': links,
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def subcategory(request, id):
    subcategory = list(Subcategory.objects.filter(id=id))[0]
    items = list(Item.objects.filter(parent__id=subcategory.id))
    template = loader.get_template('shop/subcategory.html')
    context = {
        'subcategory': subcategory,
        'items': items,
    }
    return HttpResponse(template.render(context, request))

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = str(form.cleaned_data['query'])
        items = list(Item.objects.filter(name__icontains=query))
    else:
        query = ''
        items = []
    template = loader.get_template('shop/search.html')
    context = {
        'query': query,
        'items': items
    }
    return HttpResponse(template.render(context, request))
