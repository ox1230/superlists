from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from lists.models import Item,List

def home_page(request:HttpRequest):
    return render(request, 'home.html')
def view_list(request:HttpRequest, list_id):
    list_ = List.objects.get(id = list_id)
    items = Item.objects.filter(list = list_)
    
    return render(request, "list.html",{
        'items' : items,
    })

def new_list(request:HttpRequest):
    list_ = List.objects.create()
    Item.objects.create(text = request.POST['item_text'], list = list_)
    return redirect('{}/'.format(list_.id))

