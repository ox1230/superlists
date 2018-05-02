from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from lists.models import Item

def home_page(request:HttpRequest):
    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        return redirect('lists/only_list/')
    else:
        items = Item.objects.all()
        return render(request, "home.html",{
            'items' : items,
        })

def view_list(request:HttpRequest):
        
    items = Item.objects.all()
    return render(request, "list.html",{
        'items' : items,
    })
