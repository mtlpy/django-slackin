import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'NOPE'
DEBUG = True
INSTALLED_APPS = ['django_slackin_public']
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
}]
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

SLACKIN_TOKEN = 'SLACKTOKEN'  # create a token at https://api.slack.com/web
SLACKIN_SUBDOMAIN = 'yourteam'  # if https://your-team.slack.com
