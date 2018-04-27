from django.shortcuts import render
from django.http import HttpResponse


def home_page(request) -> HttpResponse:
    return HttpResponse('<html> <title>To-Do lists</title></html>')