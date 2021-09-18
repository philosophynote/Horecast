from django.contrib import admin
from .models import Horse,Predict,Race,Result,Sanrenpuku,Sanrentan,Umaren,Umatan


@admin.register(Horse)
class HorseAdmin(admin.ModelAdmin):
    list_display = ("race_id", "horse_id", "frame_number", "horse_number","horse_name",)
    exclude = ('id',)
    list_display_links = ("race_id", )
    ordering = ("race_id","horse_number",)



@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('race_id','race_date','race_park','race_number','race_name',)
    list_display_links = ('race_id',)

@admin.register(Predict)
class PredictAdmin(admin.ModelAdmin):
    list_display = ('race_id','horse_number','pred','center','bet',)
    list_display_links = ('race_id',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('race_id','rank','horse_number','favorite','odds',)
    list_display_links = ('race_id',)






