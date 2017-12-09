#-*- coding: utf-8

#Здесь описаны только изменения в файле settings.py.
#Все остальое без имеенений
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # добавляем новое приложение
    'app_name',



]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', #тип БД (я работаю с POSTGRESQL)
        'NAME': 'default',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    #Вторая БД которую добавляем
    'data_base':{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',#тип БД (я работаю с POSTGRESQL)
        'NAME': 'Имя базы данных, которую будете использовать',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',

    }
}

#добавляем путь к классу, который описывает роутинг
#Это определяет возможность записи в другу базу данных
DATABASE_ROUTERS = ['app_name.routers.DBRouter',]
