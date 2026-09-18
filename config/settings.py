import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# 환경변수 로드 (.env)
load_dotenv(BASE_DIR / '.env')

# 보안 키
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS & CSRF 설정
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# 공공 데이터 API 키 설정 (습도 지도 서비스용)
DATA_GO_KR_API_KEY = os.getenv('DATA_GO_KR_API_KEY')

# 카카오 지도 API 키 설정 (습도 지도 서비스용)
KAKAO_MAP_CLIENT_ID = os.getenv('KAKAO_MAP_CLIENT_ID')

CSRF_TRUSTED_ORIGINS = [
    origin.strip() 
    for origin in os.getenv('CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1,http://localhost').split(',') 
    if origin.strip()
]


# 2. Application Definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'cloudinary_storage',
    'cloudinary',
    'django_htmx',

    # Local Apps
    'humidity',
    'board',
    'albums',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database: Neon PostgreSQL 연동
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True
    )
}


# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True


# Static & Media Files (WhiteNoise & Cloudinary)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Cloudinary 설정
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', '')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', '')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
}

# Django 4.2+ Storage Engine 설정
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SESSION_COOKIE_AGE = 1800 #30분(1800초) 동안 활동(요청)이 없으면 세션 만료
SESSION_EXPIRE_AT_BROWSER_CLOSE = True #브라우저를 완전히 닫으면 쿠키(세션) 삭제
SESSION_SAVE_EVERY_REQUEST = True #요청이 발생할 때마다 세션 만료 시간을 30분으로 갱신 (마지막 활동 기준 30분 연장)

# Production Security Settings (Render 배포 시 자동 적용)
if not DEBUG:    
    SECURE_SSL_REDIRECT = True # 모든 HTTP 요청을 안전한 HTTPS 요청으로 자동 리다이렉트 (HTTPS 강제)    
    SESSION_COOKIE_SECURE = True # 세션 쿠키를 HTTPS 연결을 통해서만 전송 (네트워크 도청을 통한 세션 하이재킹 방지)
    CSRF_COOKIE_SECURE = True # CSRF 토큰 쿠키를 HTTPS 연결을 통해서만 전송 (CSRF 공격 방어 강화)
    SECURE_BROWSER_XSS_FILTER = True # 브라우저의 내장 XSS(크로스 사이트 스크립팅) 필터를 활성화
    SECURE_CONTENT_TYPE_NOSNIFF = True # 브라우저가 파일의 MINE 타입을 추측(MIME Sniffing)하지 못하게 차단(잘못된 파일 확장자로 인한 악성 스크립트 실행 방지)
    SECURE_HSTS_SECONDS = 31536000  # 1 year # HSTS(Strict-Transport-Security) 헤더 설정: 1년(31,536,000초) 동안 브라우저가 이 사이트에 HTTPS로만 접속하도록 강제
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True # HSTS 정책을 모든 서브도메인(예: api.example.com, blog.example.com 등)까지 확장 적용
    SECURE_HSTS_PRELOAD = True # 브라우저의 HSTS Preload 리스트에 등록할 수 있도록 허용(사용자가 처음 방문할 때부터 HTTP 접속을 아예 차단하고 HTTPS로 연결)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # 프록시(Render, Nginx, AWS ALB 등) 뒷단에서 실행될 때, 프록시가 넘겨준 X-Forwarded-Proto 헤더를 읽어 현재 요청이 HTTPS인지 정상 판별하도록 설정

