from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('<int:pk>/', views.post_detail, name='detail'),
    path('create/', views.post_create, name='create'),    
    path('<int:pk>/update/', views.post_update, name='update'),
    path('<int:pk>/delete/', views.post_delete, name='delete'),    
]