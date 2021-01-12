from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from shop.models import Item, Category, Subcategory, Order
import random
from collections import OrderedDict

from .forms import SearchForm, OrderForm, SubmitOrderForm
from nulldorado.router import get_rnd_up_db
from django.db import transaction, IntegrityError

from time import sleep

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


def _render_cart_default(request,context:dict):
    cart_ids = request.session.get('cart',OrderedDict())
    cart_len = len(cart_ids)
    cart = OrderedDict()
    for i in cart_ids:
        item = Item.objects.get(id=i)
        if (cart_ids[i] > 0 and item.available > 0):
            cart[item] = [cart_ids[i], OrderForm(itemid=i)]
    template = loader.get_template('shop/cart.html')
    total_sum = sum(item.price * cart_ids[str(item.id)] for item in cart)
    context.update( {
        'cart_len': cart_len,
        'cart': cart,
        'total_sum' : total_sum
    })
    return HttpResponse(template.render(context, request))

def cart(request):
    return _render_cart_default(request,{})

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

def submit_order_transaction(db_name:str,cart,form):
    ids = cart.keys()
    items_for_update = list(Item.objects.using(db_name).select_for_update().filter(id__in=ids))
    items_for_update = list(zip(items_for_update,cart.values()))
    item_cnt_ok = True
    for item,item_cnt in items_for_update:
        item_cnt_ok = item_cnt_ok and item.available >= item_cnt
    if item_cnt_ok:
        order = Order.objects.create(
            phone=form.cleaned_data['number'],
            email=form.cleaned_data['email'],
            items=cart,
            address=form.cleaned_data['address'],
            order_status=Order.OrderStatus.NEW)
        order.save(using=db_name)
        for item,item_cnt in items_for_update:
            item.available -= item_cnt
            item.save(using=db_name)
    return item_cnt_ok

def submit_order(request):
    if request.method == 'POST':
        form = SubmitOrderForm(request.POST)
        cart = request.session.get('cart',OrderedDict())
        cart_empty = len(cart) == 0
        item_cnt_ok = True
        if not cart_empty and form.is_valid():
            db_name = get_rnd_up_db()
            attempts = 0
            while attempts < 3:
                try:
                    with transaction.atomic(using=db_name):
                        item_cnt_ok = submit_order_transaction(db_name,cart,form)
                    attempts = 10
                except Exception:
                    attempts += 1
                    print('=======deadlock==========',attempts)
                    sleep(0.4)
            if item_cnt_ok:
                request.session['cart'] = {}
                request.session.modified = True
                template = loader.get_template('shop/submit_order.html')
                context = {
                    'cart_len': 0,
                    'cart': {},
                    'total_sum': 0
                }
                return HttpResponse(template.render(context, request))
        if not item_cnt_ok:
            form.add_error(None,'Число товаров в корзине не должно превышать складские запасы.')
        if cart_empty:
            form.add_error(None,'Корзина пуста. Обновите страницу.')
        return _render_cart_default(request,{'form':form})


