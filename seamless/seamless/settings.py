"""
Django settings for seamless project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zixc1k$i$z17y&))$q7ta+(tb*8nt@e^vn5^dzrj*0-=l8oytj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'oauth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'seamless.urls'

WSGI_APPLICATION = 'seamless.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# my constants
CONSTANTS = {
	'CLIENT_ID': 'my app client id from azure ad',
	'CLIENT_KEY': 'my app client key from azure ad',
	'STEP_1_TEMPLATE_NAME': 'oauth/step1.html',
	'STEP_2_TEMPLATE_NAME': 'oauth/step2.html',
	'REDIRECT_URI': 'http://localhost:8000/oauth/step2/',
	'AUTHORIZATION_BASE_URL': 'https://login.windows.net/%s/oauth2/authorize',
	'BASE_TOKEN_URL': 'https://login.windows.net/%s/oauth2/token',
	'RESOURCE_URI': 'https://management.core.windows.net/',
	'GET_SUBSCRIPTIONS_URL': 'https://management.core.windows.net/subscriptions',
	'MS_API_VERSION_HEADER': 'x-ms-version',
	'MS_API_VERSION_HEADER_VALUE': '2013-08-01'
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
