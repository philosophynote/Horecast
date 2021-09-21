from django.urls import path,include
from . import views

app_name = 'forecast'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('manage', views.manage, name='manage'),
    path('search', views.search, name='search'),
    path('upload', views.upload, name='upload'),
    path('timeline', views.Timeline.as_view(), name='timeline'),
    path('scrape_rc', views.scrape_rc, name='scrape_rc'),
    path('toppage', views.Toppage.as_view(), name='toppage'),

]
