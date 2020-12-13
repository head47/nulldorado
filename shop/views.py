from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from shop.models import Item, Category, Subcategory
import random
from collections import OrderedDict

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
    context = {
        'links': links
    }
    return HttpResponse(template.render(context, request))
