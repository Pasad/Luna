# humidity/views.py
from django.shortcuts import render
from django.conf import settings
from .services import fetch_humidity_data

def humidity_map_view(request):
    """제주 전체 지역 실시간 습도 지도 화면"""
    humidity_list = fetch_humidity_data()  # DB 내 모든 지역 조회

    context = {
        'humidity_list': humidity_list,
        'kakao_map_client_id': settings.KAKAO_MAP_CLIENT_ID,
    }

    return render(request, 'humidity/index.html', context)