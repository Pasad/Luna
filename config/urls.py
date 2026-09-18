# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    
    path('accounts/', include('django.contrib.auth.urls')), # 내장 로그인/로그아웃 URL 연동
    path('humidity/', include('humidity.urls')),
    path('board/', include('board.urls')),
    path('albums/', include('albums.urls')),    
]