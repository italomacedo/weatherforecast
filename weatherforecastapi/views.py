from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import forecast

def index(request):
    context_params = {'version':"1.1"}
    return render(request, 'index.html', context=context_params)

def api(request):
    accountId = request.GET.get('accountId')
    futureDate = request.GET.get('futureDate')

    predicts = forecast.predict(accountId, futureDate)

    return HttpResponse(predicts.to_json())