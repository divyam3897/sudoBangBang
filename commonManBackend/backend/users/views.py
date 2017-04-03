from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from categories.models import *
from users.models import *

@csrf_exempt
def register(request):
    data = json.loads(request.body.decode('utf-8'))
    name = data['name']
    username = data['userName']
    password = data['password']
    email = data['email']
    number = data['number']
    address = data['address']
    user = User(username=username,email=email,first_name=name)
    user.set_password(password)
    user.save()

@csrf_exempt
def loginView(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
            return JsonResponse({"status":"LoggedIn"})
        else:
            print("no user")
    else:
        return JsonResponse({"status":"Invalid details"})

@csrf_exempt
def addItem(request):
    data = json.loads(request.body.decode('utf-8'))
    itemName = data['item']
    item = categoryItem.objects.get(itemName=itemName)
    cartItem = cart(item=item,user=request.user)
    cartItem.save()
    return JsonResponse({"status":"Item added"})

@csrf_exempt
def cartItems(request):
    itemDetails = cart.objects.filter(user= request.user)
    # print(itemDetails)
    allItems = {}
    items = []
    for i in itemDetails:
        # items.append(i.item.name)
        # print(i.item.price)
        allItems['name'] = i.item.itemName # = {
                # "image": i.item.image,
                # "price": i.item.price,
                # }
    # allItems['item'] = items
    print(allItems)
    return JsonResponse(allItems)

@csrf_exempt
def loggedIn(request):
    if request.user.is_authenticated():
        return JsonResponse({"status":"LoggedIn"})
    else:
        return JsonResponse({"status":"Invalid details"})

@csrf_exempt
def logoutView(request):
    logout(request)
    return JsonResponse({"status":"Logout out"})

