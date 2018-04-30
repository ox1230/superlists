from django.shortcuts import render
from django.http import HttpResponse


def home_page(request) -> HttpResponse:
    if request.method == "POST":
        return HttpResponse(request.POST['item.text'])
    return render(request, "home.html")