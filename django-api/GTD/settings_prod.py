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
        'NAME': os.environ.get('gtd-mysql-1'),
        'USER': os.environ.get('admin'),
        'PASSWORD': os.environ.get('Db_Pass!'),
        'HOST': os.environ.get('gtd-mysql-1.cghnoav6qten.us-east-1.rds.amazonaws.com'),
        'PORT': os.environ.get('3306'),
    }
}
