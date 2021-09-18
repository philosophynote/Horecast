from .forms import RaceSearchForm
from django.shortcuts import render

def searchform(request):
    result = {}
    result['form'] = RaceSearchForm()
    return  result