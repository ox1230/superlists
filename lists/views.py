from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ValidationError
from lists.models import Item,List
from lists.forms import ItemForm

def home_page(request:HttpRequest):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request:HttpRequest):
    list_ = List.objects.create()
    item = Item.objects.create(text = request.POST['text'], list = list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "빈 아이템을 등록할 수 없습니다"
        return render(request, 'home.html', {'error':error})
    return redirect(list_)

def view_list(request:HttpRequest, list_id):
    list_ = List.objects.get(id = list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item.objects.create(text = request.POST['text'], list = list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        
        except ValidationError:
            item.delete()
            error = "빈 아이템을 등록할 수 없습니다"
    
    return render(request, "list.html",{
        'list' : list_,
        'error':error
    })

