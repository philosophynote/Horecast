from django.contrib import admin
from django.urls import path,include

from forecast import views

# handler500 = views.my_customized_server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forecast.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
