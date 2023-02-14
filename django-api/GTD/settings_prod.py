from .settings import *

# Override settings for production environment
DEBUG = True

ALLOWED_HOSTS = [
    'budatask.com',
    'www.budatask.com',
    ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gtd',
        'USER': 'admin',
        'PASSWORD': 'Db_Pass!',
        'HOST': 'gtd-mysql-1.cghnoav6qten.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}
