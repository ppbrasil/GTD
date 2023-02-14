from .settings import *

# Override settings for production environment
DEBUG = False

ALLOWED_HOSTS = [
    'www.budatask.com',
    'budatask.com',
    ]

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('django.db.backends.mysql'),
        'NAME': os.environ.get('django_db'),
        'USER': os.environ.get('django_user'),
        'PASSWORD': os.environ.get('secret'),
        'HOST': os.environ.get('db'),
        'PORT': os.environ.get('3306'),
    }
}
