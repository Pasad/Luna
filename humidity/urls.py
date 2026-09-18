from django.urls import path
from . import views

app_name = 'humidity'

urlpatterns = [
    path('', views.humidity_map_view, name='map'),
]