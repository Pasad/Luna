from django.urls import path
from . import views

app_name = 'albums'

urlpatterns = [
    path('', views.album_list, name='list'),
    path('create/', views.album_create, name='create'),
    path('<int:pk>/update/', views.album_update, name='update'),
    path('<int:pk>/delete/', views.album_delete, name='delete'),
]