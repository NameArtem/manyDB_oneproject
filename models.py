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