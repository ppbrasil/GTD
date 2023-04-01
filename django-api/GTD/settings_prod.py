from .settings import *

# Override settings for production environment
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '172.31.4.18',
    'www.budatask.com',
    'budatask.com',
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
