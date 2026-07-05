import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += [
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'django_cleanup.apps.CleanupConfig',
    'corsheaders',

    # Local apps
    'core',
    'user',
    'project',
    'investment',
    'evaluation_request',
    'notification',
    'support',
    'docs',
    'blog',
]

JAZZMIN_SETTINGS = {
    "site_title": "Winners Regional Center",
    "site_header": "Winners Regional Center",
    "site_brand": "WRC Admin",
    "site_logo": None,
    "login_logo": None,
    "welcome_sign": "Welcome to Winners Regional Center Admin",
    "copyright": "Winners Regional Center",

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "user",
        "evaluation_request",
        "project",
        "investment",
        "docs",
        "blog",
        "support",
        "notification",
        "core",
        "auth",
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.Group": "fas fa-users",

        "user": "fas fa-user-circle",
        "user.User": "fas fa-user",
        "user.OTP": "fas fa-key",
        "user.PasswordResetToken": "fas fa-lock",

        "evaluation_request": "fas fa-clipboard-check",
        "evaluation_request.EvaluationRequest": "fas fa-file-signature",

        "project": "fas fa-building",
        "project.Project": "fas fa-city",

        "investment": "fas fa-hand-holding-usd",
        "investment.Investment": "fas fa-chart-line",

        "docs": "fas fa-folder-open",
        "docs.RequiredDocument": "fas fa-file-alt",
        "docs.UserDocument": "fas fa-file-contract",

        "blog": "fas fa-newspaper",
        "blog.BlogPost": "fas fa-blog",

        "support": "fas fa-headset",
        "support.SupportQuery": "fas fa-question-circle",
        "support.SupportReply": "fas fa-reply",

        "notification": "fas fa-bell",
        "notification.Notification": "fas fa-bullhorn",

        "core": "fas fa-cogs",
        "core.BusinessSetting": "fas fa-sliders-h",
    },

    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["user.view_user"]},
        {"name": "View Website", "url": "/", "new_window": True},
    ],

    "show_ui_builder": False,
}

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WinnersRegionalCenter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'WinnersRegionalCenter.wsgi.application'


import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(
        f"{os.getenv('DB_URL')}"
        
    )
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'core.renderers.EnvelopedJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    "DEFAULT_PAGINATION_CLASS": "core.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    "EXCEPTION_HANDLER": "core.exceptions.custom_exception_handler",
    "DEFAULT_RENDERER_CLASSES": ["core.renderers.StandardRenderer"],
    "DEFAULT_THROTTLE_RATES": {
        "user": "60/min",
        "anon": "5/min",
        "contact_form": "10/hour",
        "forgot_password": "3/hour",
        "resend_otp": "3/hour",
        "verify_reset_otp": "10/hour",
    },
}

OTP_EXPIRY_MINUTES = 10
OTP_MAX_ATTEMPTS = 5
PASSWORD_RESET_TOKEN_EXPIRY_MINUTES = 10


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = f"WinnerRegionalCenter <{os.getenv('EMAIL_HOST_USER')}>"


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Winners Regional Center API',
    'DESCRIPTION': 'API documentation for Winners Regional Center.',
    'VERSION': '1.0.0',
    # 'SERVE_INCLUDE_SCHEMA': False,
}

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "x-csrftoken",
]

CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',') if origin.strip()]
