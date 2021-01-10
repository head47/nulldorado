from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from shop.models import Item, Category, Subcategory, Order
import random
from collections import OrderedDict

from .forms import SearchForm, OrderForm, SubmitOrderForm

def index(request):
    cart_len = len(request.session.get('cart',[]))
    newItems = list(Item.objects.filter(new=True))
    showcase = random.sample(newItems, 3)
    template = loader.get_template('shop/index.html')
    form = SearchForm()
    context = {
        'showcase': showcase,
        'form': form,
        'cart_len': cart_len,
    }
    return HttpResponse(template.render(context, request))

def catalogue(request):
    cart_len = len(request.session.get('cart',[]))
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
        'cart_len': cart_len,
    }
    return HttpResponse(template.render(context, request))

def subcategory(request, id):
    cart_len = len(request.session.get('cart',[]))
    subcategory = list(Subcategory.objects.filter(id=id))[0]
    items = list(Item.objects.filter(parent__id=subcategory.id))
    forms = {}
    for i in items:
        forms[i] = OrderForm(itemid=i.id)
    template = loader.get_template('shop/subcategory.html')
    context = {
        'subcategory': subcategory,
        'cart_len': cart_len,
        'forms': forms,
    }
    return HttpResponse(template.render(context, request))

def search(request):
    cart_len = len(request.session.get('cart',[]))
    form = SearchForm(request.GET)
    if form.is_valid():
        query = str(form.cleaned_data['query'])
        items = list(Item.objects.filter(name__icontains=query))
    else:
        query = ''
        items = []
    forms = {}
    for i in items:
        forms[i] = OrderForm(itemid=i.id)
    template = loader.get_template('shop/search.html')
    context = {
        'query': query,
        'forms': forms,
        'cart_len': cart_len,
    }
    return HttpResponse(template.render(context, request))

def contacts(request):
    cart_len = len(request.session.get('cart',[]))
    template = loader.get_template('shop/contacts.html')
    context = {
        'cart_len': cart_len,
    }
    return HttpResponse(template.render(context, request))

def about(request):
    cart_len = len(request.session.get('cart',[]))
    template = loader.get_template('shop/about.html')
    context = {
        'cart_len': cart_len,
    }
    return HttpResponse(template.render(context, request))

def cart(request):
    cart_ids = request.session.get('cart',OrderedDict())
    cart_len = len(cart_ids)
    cart = OrderedDict()
    for i in cart_ids:
        cart[Item.objects.get(id=i)] = [cart_ids[i], OrderForm(itemid=i)]
    template = loader.get_template('shop/cart.html')
    context = {
        'cart_len': cart_len,
        'cart': cart,
    }
    return HttpResponse(template.render(context, request))

def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cart = request.session.get('cart',OrderedDict())
            item = Item.objects.get(id=form.cleaned_data['id'])
            amount = form.cleaned_data['amount']
            if amount == 0:
                cart.pop(str(item.id), None)
            else:
                cart[item.id] = amount
            request.session['cart'] = cart
            request.session.modified = True
    return HttpResponseRedirect('/cart')

def submit_order(request):
    if request.method == 'POST':
        form = SubmitOrderForm(request.POST)
        if form.is_valid():
            cart = request.session.get('cart',OrderedDict())
            Order.objects.create(phone=form.cleaned_data['number'],email=form.cleaned_data['email'],items=cart)
            for item_id, item_cnt in cart.items():
                item = Item.objects.get(id=item_id)
                item.available = item.available - item_cnt if item_cnt <= item.available else 0
                item.save()
            request.session['cart'] = {}
            request.session.modified = True
            template = loader.get_template('shop/submit_order.html')
            context = {
                'cart_len': 0,
                'cart': {},
            }
            return HttpResponse(template.render(context, request))
        
        #code identical to card
        cart_ids = request.session.get('cart',OrderedDict())
        cart_len = len(cart_ids)
        cart = OrderedDict()
        for i in cart_ids:
            cart[Item.objects.get(id=i)] = [cart_ids[i], OrderForm(itemid=i)]
        template = loader.get_template('shop/cart.html')
        context = {
            'cart_len': cart_len,
            'cart': cart,
            'form':form
        }
        return HttpResponse(template.render(context, request))