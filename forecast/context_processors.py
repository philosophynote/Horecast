from .forms import RaceSearchForm
from django.shortcuts import render
from .models import Race
import datetime

def race_search(request):
    return  {
        'result':RaceSearchForm()
        }

def date(request):
    race_id= Race.objects.latest("race_date")
    race = Race.objects.filter(race_id=race_id).first()
    race_date = datetime.datetime.strptime(race.race_date, "%Y/%m/%d")
    context = {
        "RACE_DATE":race_date,
    }
    return context



