from django.shortcuts import render
from django.http import Http404


def home_view(request):
    return render(request, 'home.html')


def custom_404_view(request):
    return render(request, '404.html')
