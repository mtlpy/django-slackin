import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'NOPE'
DEBUG = True
INSTALLED_APPS = ['django_slackin_public']
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

SLACKIN_TOKEN = 'YOUR-SLACK-TOKEN'  # create a token at https://api.slack.com/web
SLACKIN_SUBDOMAIN = 'your-team'  # if https://your-team.slack.com
