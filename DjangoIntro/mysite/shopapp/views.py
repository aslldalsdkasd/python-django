from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


# Create your views here.

def index(request: HttpRequest):
    list_things = [
        ('Smartphone', 3000),
        ('Laptop', 500),
    ]
    numbers = [
        1,2,3,4,5,6
    ]
    context = {
        'list_things':list_things,
        'numbers':numbers,
    }
    return render(request, 'shopapp/index.html', context=context)
