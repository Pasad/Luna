import requests
from datetime import datetime, timedelta
from django.conf import settings
from .models import JejuWeather

def get_base_date_time():
    """기상청 API 호환 기준 날짜 및 시간 계산"""
    now = datetime.now()
    if now.minute < 15:
        now -= timedelta(hours=1)
    
    base_date = now.strftime('%Y%m%d')
    base_time = now.strftime('%H00')
    return base_date, base_time

def fetch_humidity_data(region_id=None):
    """
    DB의 지역별 지점 데이터를 기반으로 
    기상청 API를 호출해 제주 지역별 습도 데이터를 반환
    """
    api_key = settings.DATA_GO_KR_API_KEY
    base_date, base_time = get_base_date_time()
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

    # DB에서 조회 대상 가져오기
    if region_id and region_id != 'all':
        locations = JejuWeather.objects.filter(id=region_id)
    else:
        locations = JejuWeather.objects.all()

    results = []

    for loc in locations:
        humidity_val = None
        
        if api_key:
            params = {
                'serviceKey': api_key,
                'pageNo': '1',
                'numOfRows': '10',
                'dataType': 'JSON',
                'base_date': base_date,
                'base_time': base_time,
                'nx': loc.nx,
                'ny': loc.ny,
            }
            try:
                response = requests.get(url, params=params, timeout=5)
                data = response.json()
                items = data['response']['body']['items']['item']
                
                for item in items:
                    if item['category'] == 'REH':
                        humidity_val = int(item['obsrValue'])
                        break
            except Exception:
                pass

        # API 호출 실패 또는 키 미설정 시 'N/A' 적용
        if humidity_val is None:
            humidity_val = 'N/A'

        results.append({
            'id': loc.id,
            'region': loc.name,
            'lat': loc.lat,
            'lng': loc.lng,
            'humidity': humidity_val,
            'status': get_humidity_status(humidity_val),
            'updated_at': f"{base_date[:4]}-{base_date[4:6]}-{base_date[6:]} {base_time[:2]}:00"
        })

    return results

def get_humidity_status(humidity):
    """습도 값에 따른 상태 표시 (N/A 및 미조회 예외 처리)"""
    if humidity == 'N/A' or humidity is None or not isinstance(humidity, (int, float)):
        return {'label': '정보 없음', 'color': 'text-gray-500', 'bg': 'bg-gray-100', 'border': 'border-gray-200'}
    
    if humidity < 40:
        return {'label': '건조', 'color': 'text-amber-600', 'bg': 'bg-amber-50', 'border': 'border-amber-200'}
    elif 40 <= humidity <= 60:
        return {'label': '쾌적', 'color': 'text-emerald-600', 'bg': 'bg-emerald-50', 'border': 'border-emerald-200'}
    else:
        return {'label': '습함', 'color': 'text-blue-600', 'bg': 'bg-blue-50', 'border': 'border-blue-200'}