from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from shop.models import Item
import random

def index(request):
    newItems = list(Item.objects.filter(new=True))
    showcase = random.sample(newItems, 3)
    template = loader.get_template('shop/index.html')
    context = {
        'showcase': showcase,
    }
    return HttpResponse(template.render(context, request))
