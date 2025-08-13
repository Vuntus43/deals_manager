import os
from integration_utils.its_utils.mute_logger import MuteLogger
APP_SETTINGS = None

ADMINS = (('img', 'img@it-solution.ru'),)

BASE_DOMAIN = 'https://deals_manager.it-solution.ru'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(__file__).replace('\\', '/')

SECRET_KEY = 'django-insecure-rnle!o0cd6)ka-o%0ra3t1o1y@jrf%+@s5v8pajp3iq!w-#6$i'

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'deals_app',

    'integration_utils.bitrix24',
    'integration_utils.its_utils.app_gitpull',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'deals_manager.urls'

CSRF_TRUSTED_ORIGINS = [
    'https://*.bitrix24.ru',                         # все порталы Б24
    'https://b24-q0k90e.bitrix24.ru',                # твой конкретный портал (на всякий случай)
    'http://127.0.0.1:8000',                         # локалка
    # 'https://<твой-ngrok>.ngrok-free.app',         # если идёшь через https/ngrok
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'deals_manager.wsgi.application'

# -------------------- БАЗА ДАННЫХ: Postgres --------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'foodgram',  # Or path to database file if using sqlite3.
        'USER': 'postgres',  # Not used with sqlite3.
        'PASSWORD': 'Vanek2004!',  # Not used with sqlite3.
        'HOST': 'localhost',
    },
}

# -------------------- ПАРОЛИ --------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------- ЛОКАЛИ --------------------
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -------------------- СТАТИКА/МЕДИА --------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
ENTRY_FILE_UPLOADING_FOLDER = os.path.join(MEDIA_ROOT, 'uploaded_entrie_files')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

# -------------------- IFRAME + COOKIE --------------------
# Для локального HTTP (без https) поставь False, для https (ngrok/домена) — True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True   # <- включи True, если открываешь по HTTPS
CSRF_COOKIE_SECURE = True      # <- включи True, если открываешь по HTTPS
# X_FRAME_OPTIONS = 'ALLOWALL'

# -------------------- ЛОГГЕР ИЗ utils --------------------
ilogger = MuteLogger()

# -------------------- LOCAL SETTINGS --------------------
try:
    from deals_manager.local_settings import *  # здесь должен задаваться APP_SETTINGS = LocalSettingsClass(...)
except ImportError:
    from warnings import warn
    warn('create deals_manager/local_settings.py with APP_SETTINGS')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
