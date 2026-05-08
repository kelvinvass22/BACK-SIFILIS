import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-2_emy^)#y*2n5@4p2bo3e)wc952b9-kn07!(+=i%70)_8)8zek')
DEBUG = config('DEBUG', default=True, cast=bool) # No Render, coloque DEBUG=False nas variáveis

ALLOWED_HOSTS = ['*', 'back-sifilis.onrender.com', 'localhost', '127.0.0.1', '10.0.2.2']
APPEND_SLASH = True

AUTH_USER_MODEL = 'accounts.User'
SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount', 
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'drf_spectacular',
    'corsheaders',
    'storages',
    'apps.accounts',
    'apps.content',
    'apps.qna',
    'apps.gamification',
]

ACCOUNT_ADAPTER = 'apps.accounts.adapters.CustomAccountAdapter'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '' 
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'apps/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://postgres:postgres@db:5432/postgres',
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Fortaleza'
USE_I18N = True
USE_TZ = True

# Cloudflare R2 / S3
AWS_ACCESS_KEY_ID = config("CLOUDFLARE_R2_ACCESS_KEY", default="")
AWS_SECRET_ACCESS_KEY = config("CLOUDFLARE_R2_SECRET_KEY", default="")
AWS_S3_ENDPOINT_URL = config("CLOUDFLARE_R2_BUCKET_ENDPOINT", default="")
AWS_STORAGE_BUCKET_NAME = config("CLOUDFLARE_R2_BUCKET", default="")
AWS_S3_REGION_NAME = "auto"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE = False
AWS_S3_CUSTOM_DOMAIN = config("AWS_S3_CUSTOM_DOMAIN", default="pub-1293c24e889b457f83d56dbc02ce5123.r2.dev")

STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CONFIGURAÇÃO DE E-MAIL À PROVA DE ERRO 500

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.resend.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# No Resend, o usuário é fixo, o que muda é a senha (API KEY)
EMAIL_HOST_USER = 'resend'
EMAIL_HOST_PASSWORD = os.environ.get('RESEND_API_KEY')

# No plano gratuito, você SÓ PODE usar este remetente:
DEFAULT_FROM_EMAIL = 'onboarding@resend.dev'

# Deixamos False para você ver se o erro mudou caso falhe
EMAIL_FAIL_SILENTLY = False

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}

SIMPLE_JWT = {
    'TOKEN_OBTAIN_SERIALIZER': 'apps.accounts.serializers.MyTokenObtainPairSerializer',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
}

REST_AUTH = {
    'USE_JWT': True,
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'apps.accounts.serializers.CustomPasswordResetConfirmSerializer',
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "https://back-sifilis.onrender.com", 
    "http://localhost:8000", 
    "http://127.0.0.1:8081",
    "http://localhost:8081"
]