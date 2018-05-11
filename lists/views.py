from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ValidationError
from lists.models import Item,List

def home_page(request:HttpRequest):
    return render(request, 'home.html')

def view_list(request:HttpRequest, list_id):
    list_ = List.objects.get(id = list_id)
    
    return render(request, "list.html",{
        'list' : list_,
    })

def new_list(request:HttpRequest):
    list_ = List.objects.create()
    item = Item.objects.create(text = request.POST['item_text'], list = list_)
    try:
        item.full_clean()
    except ValidationError:
        error = "빈 아이템을 등록할 수 없습니다"
        return render(request, 'home.html', {'error':error})
    return redirect('{}/'.format(list_.id))

def add_item(request:HttpRequest, list_id):
    list_ = List.objects.get(id = list_id)
    Item.objects.create(text = request.POST['item_text'], list = list_)
    
   

    return redirect('/lists/{}/'.format(list_.id))
