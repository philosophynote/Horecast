from .forms import RaceSearchForm
from django.shortcuts import render
from .models import Race,BeforeComment
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

# def forecast_card(request):
#     forecast = BeforeComment.objects.all().order_by('-created_at').first()
#     race_date = datetime.datetime.strptime(forecast.race.race_date, "%Y/%m/%d")
#     forecast_list = {
#         "FORECAST":forecast,
#         "forecast_date":race_date,
#     }
#     return forecast_list



