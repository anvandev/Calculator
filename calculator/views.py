from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'calculator/main.html')


def calculate(request):
    expression = request.GET['expression']
    return HttpResponse(expression)
