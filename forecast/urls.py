from django.urls import path,include
from . import views
from . import dashboard

app_name = 'forecast'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('race', views.Racelist.as_view(), name='race'),
    path('manage', views.manage, name='manage'),
    path('search', views.search, name='search'),
    path('upload', views.upload, name='upload'),
    path('judgecomment', views.judgecomment, name='judgecomment'),
    path('timeline', views.Timeline.as_view(), name='timeline'),
    path('choice_race', views.ChoiceRace.as_view(), name='choice_race'),
    path('create_beforecomment/<str:race_id>', views.CreateBeforeComment.as_view(), name='create_beforecomment'),
    path('detail_beforecomment/<int:pk>/', views.DetailBeforeComment.as_view(), name='detail_beforecomment'),
    path('update_beforecomment/<int:pk>/', views.UpdateBeforeComment.as_view(), name='update_beforecomment'),
    path('delete_beforecomment/<int:pk>/', views.DeleteBeforeComment.as_view(), name='delete_beforecomment'),
    path('create_aftercomment/<int:pk>', views.CreateAfterComment.as_view(), name='create_aftercomment'),
    path('delete_aftercomment/<int:pk>/', views.DeleteAfterComment.as_view(), name='delete_aftercomment'),
    path('scrape_rc', views.scrape_rc, name='scrape_rc'),
    path('race_detail/<str:race_id>/', views.RaceDetail.as_view(), name='race_detail'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('forecast_search', views.search_forecast, name='forecast_search'),
]
