from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    context_params = {'version':"1.1"}
    return render(request, 'index.html', context=context_params)