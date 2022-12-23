from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def overview(request):
    data = [1, 2, 3]
    return HttpResponse(data)

def category_data(request):
    data = [4, 5, 6]
    return HttpResponse(data)



