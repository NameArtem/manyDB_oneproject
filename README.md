# manyDB_oneproject
This is a simple way for using two or more DataBases in one Django Projec
-----------------------------------------------------------------------------------------------------
Простой способ, чтобы использовать в вашем Django проекте две и более базы данных.
Последовательность выполнения работ:

1. Создаем приложение, которое будет использовать сторонную базу данных:
python manage.py startapp app_name





2. Исправляем файл settings.py. Добавляем туда ещё одну базу данных в DATABASE:
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




3. Добавляем модели из новой базы данных в файл app_name/models.py (если в базе данных уже есть даные, но можно сделать этот шаг, даже если она без таблиц)
python manage.py inspectdb --database=data_base > app_name/models.py




4. Файл app_name/models.py изменится(если в базе были таблицы), будет содержать модели с существующими таблицами. Их можно исправить и дополнить. Пример файла app_name/models.py:
#-*- coding: utf-8
from __future__ import unicode_literals
from django.db import models

#Здесь будут показаны все модели после выполнения команды inspectdb
#python manage.py inspectdb --database=your_database > app_name/models.py
#
#Конечно, если база данных, которую вы подключаете уже имеет таблицы
#

#таблица которая уже была в добавляемоей базе данных:
#отображение класса, называется так же, как таблица в базе данный
class City(models.Model):
    #столбец ID пропуще, так как он автоматически заполняется при появлении новой записи
    #имя столбца и определение в нем имени колонки, куда он записан (db_column)
    name = models.CharField(max_length=250, blank=True, null=True, db_column='name')

    #отображение в админки
    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        managed = False     #Обозначение того, что Django не создаст этой таблице при выполнении migrate
        db_table = u'city'  #обозначение имяни таблицы

#Внимание, что если полей будет много
#и параметров в них тоже будет много, то стоит проиверять и дописывать параметры
#такие как: поле foreign_key, ManyToMany и т.п.




5. Теперь необходимо создать файл app_name/routers.py и описать в нем класс, который будет отвечать за роутинг. Если сделать ошибку в этой файле с определениями имени базы данных или имени приложения, то модели будут регистрироваться в интерфейсе администратора, !НО! при обращении к ним будет следующая ошибка:
Exception Value: relation "имя таблицы" does not exist 
LINE 1: SELECT COUNT(*) AS "__count" FROM "имя таблицы"

Пример содержания файла app_name/routers.py:
#-*- coding: utf-8
#этот файл, что бы перекидывались данные из app_name в базу данных
#app_name - имя приложения
#data_base - имя вашей другой базы данных, которую вы подключили в settings.py DATABASE

class DBRouter(object):

    #определение  базы данных для чтения
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'app_name':
            return 'data_base'
        return 'default'

    #определение базы данных для записи
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'app_name':
            return 'data_base'
        return 'default'    #основная база данных из settings.py

    #выполнение оперцаии проверки и определение возможности организации связи между объектами
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'app_name' and obj2._meta.app_label == 'app_name':
            return True
        elif 'app_name' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    #определяем возможность миграции модели и базы данных
    def allow_syncdb(self, db, model):
        if db == 'data_base' or model._meta.app_label == "app_name":
            return False
        else:
            return True
           
 
 
 
 6. Определяем в settings.py роутинг, который был создан:
 
#добавляем путь к классу, который описывает роутинг
#Это определяет возможность записи в другу базу данных
DATABASE_ROUTERS = ['app_name.routers.DBRouter',]




7. Регистрируем в модель в admin.py:
#-*- coding: utf-8
from django.contrib import admin
from django.db.models.base import ModelBase
#импортируем модель из приложения
from app_name import models as m

#Если моделей много, можно использовать хитрость
#что бы зарегистрировать в админке все модели сразу:
for name,value in m.__dict__.items():
    if type(value) is ModelBase:
        admin.site.register(value)
              
#или зарегистрировать только необходимые модели / модель
admin.site.register(name_model)




-----------------------------------------------------------------------------------
Это все! Теперь Django работает с двумя базами данных и можно выбирать место записи.
