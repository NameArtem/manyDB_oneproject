#-*- coding: utf-8
#этот файл, что бы перекидывались данные из app_name в базу данных
#app_name - имя приложения
#data_base - имя вашей другой базы данных, которую вы подключили в settings.py DATABASE

#Внимание! Если роутинг написан не правильно
# или содержит ошибку в определениеи базы данных
# Вы будете получать ошибку "Exception Value: relation "table_name" does not exist"



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