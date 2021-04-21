import os, json
from pathlib import Path

SETTING_FOLDER_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_FOLDER_DIR = os.path.join(SETTING_FOLDER_DIR, 'confs')
BASE_DIR = Path(__file__).resolve().parent.parent.parent
AUTH_USER_MODEL = 'gmtool.Gm'

def get_json_content(file_name):
    content = None
    full_name = os.path.join(CONF_FOLDER_DIR, file_name)
    with open(full_name) as f:
        content = json.loads(f.read())
        return content
        pass
    pass

def get_val_from_json(content, key:str):
    try:
        if content is None or key is None:
            raise KeyError()
        return content[key]
        pass
    except:
        pass
    pass

# 장고 비밀키 읽기
secret_key = get_json_content('secret_key.json')
SECRET_KEY = get_val_from_json(secret_key, 'SECRET_KEY')

#장고 smtp 관련 계정 및 설정정보 읽기
smtp_key = get_json_content('smtp_key.json')
DEVELOPER_MAIL = 'sweetmeatsboy@gmail.com'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = get_val_from_json(smtp_key, 'EMAIL_HOST')
EMAIL_HOST_USER = get_val_from_json(smtp_key, 'EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_val_from_json(smtp_key, 'EMAIL_HOST_PASSWORD')
EMAIL_PORT = get_val_from_json(smtp_key, 'EMAIL_PORT')
DEFAULT_FROM_EMAIL = get_val_from_json(smtp_key, 'DEFAULT_FROM_EMAIL')

#OAuth 관련 설정정보.
oauth_key = get_json_content('auth_key.json')
# FACEBOOK OAUTH 설정값.
FACEBOOK = get_val_from_json(oauth_key, 'FACEBOOK')
GOOGLE = get_val_from_json(oauth_key, 'GOOGLE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '[::1]',
    '.pythonanywhere.com',
    '.ap-northeast-2.compute.amazonaws.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'imagekit',
    'storages',
    'gateway',
    'gmtool',
    'outstargram_drf',
    'outstargram'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_PATH,
        ],
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

WSGI_APPLICATION = 'portfolio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'
STATIC_DIR = os.path.join(BASE_DIR, '/static/')
STATICFILES_DIRS = [
    STATIC_DIR,
]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 세션 live 시간. 추후 test 환경에선 1시간으로 늘릴것.
SESSION_COOKIE_AGE = 60 * 15 # 15분으로 설정
SESSION_SAVE_EVERY_REQUEST = False

######################## media 관련
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
