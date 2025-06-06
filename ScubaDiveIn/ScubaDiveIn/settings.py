"""
Django settings for ScubaDiveIn project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config, Csv
from .timeout_settings import *  # Import all timeout settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-2n-3#t%!fum0)m#+*mdafc9*#am$zprt502llr2g2jo3rt#e0$')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default="13.61.19.80,scubadivein.in,*", cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainSite',
    'accounts',
    'imagekit',
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

ROOT_URLCONF = 'ScubaDiveIn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'course_filters': 'mainSite.templatetags.course_filters',
            }
        },
    },
]

WSGI_APPLICATION = 'ScubaDiveIn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Timeout configurations
DATABASES['default']['CONN_MAX_AGE'] = DB_CONNECT_TIMEOUT
DATABASES['default']['OPTIONS'] = {
    'timeout': DB_CONNECT_TIMEOUT,
}

# Session and cache settings
SESSION_COOKIE_AGE = SESSION_COOKIE_AGE  # From timeout_settings
CACHE_TIMEOUT = CACHE_TIMEOUT  # From timeout_settings

# API timeout settings
RAZORPAY_TIMEOUT = RAZORPAY_API_TIMEOUT  # From timeout_settings

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Razorpay Settings
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID', default='rzp_test_Sf5MAcuzRuHH3h')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET', default='XvMTRMSGBlUtaU4o3VfyTjBF')

# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'homePage'

# Email settings (for password reset and other transactional emails)
# For development, use console backend to see emails in console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production, use SMTP
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
# EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='your-email@gmail.com')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='your-app-password')

# Admin email for receiving notifications
ADMIN_EMAIL = config('ADMIN_EMAIL', default='admin@scubadivein.in')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='info@scubadivein.in')

# Base URL configuration
BASE_URL = 'http://127.0.0.1:8000'

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ImageKit Settings
IMAGEKIT_PRIVATE_KEY = 'private_MUzQsUvmxmoOtjbyTQ22f4RqQOU='
IMAGEKIT_PUBLIC_KEY = 'public_Rmn9CYcy5ESbCY4tkUFIjogNwbg='
IMAGEKIT_URL_ENDPOINT = 'https://ik.imagekit.io/7wugbzwtbb'