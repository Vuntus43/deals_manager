DEBUG = True
ALLOWED_HOSTS = ['*']

from integration_utils.bitrix24.local_settings_class import LocalSettingsClass

# Твой домен портала и адрес, по которому доступно локальное приложение
PORTAL = 'b24-q0k90e.bitrix24.ru'     # без https://
APP_DOMAIN = '127.0.0.1:8000'        # или ngrok-домен

APP_SETTINGS = LocalSettingsClass(
    portal_domain=PORTAL,
    app_domain=APP_DOMAIN,
    app_name='deals_manager',
    salt='wefiewofioiI(IF(Eufrew8fju8ewfjh-DEALS-MANAGER',
    secret_key='wefewfkji4834gudrj.kjh237tgofhfjekewf.kjewkfjeiwfjeiwjfijewf',
    application_bitrix_client_id='local.6899c881531f95.06851383',
    application_bitrix_client_secret='W21wxJeuSd5obBh2zohSCbpVwdmGUnVCV7aXUPHAaMHwDhUPnJ',
    application_index_path='/',
)

# пример переменных для интеграций (как в is_demo)
OPEN_AI_API_KEY = 'your-api-key'

# База как в is_demo; можно оставить Postgres или заменить на SQLite для локалки
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'foodgram',  # Or path to database file if using sqlite3.
        'USER': 'postgres',  # Not used with sqlite3.
        'PASSWORD': 'Vanek2004!',  # Not used with sqlite3.
        'HOST': 'localhost',
    },
}

# если используешь ngrok:
DOMAIN = "c5b354d95473.ngrok-free.app"
