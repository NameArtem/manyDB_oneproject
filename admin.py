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


