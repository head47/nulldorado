import random
from django.conf import settings
import MySQLdb

def dbUp(database_name):
    try:
        db_definition = getattr(settings, 'DATABASES')[database_name]
        db = MySQLdb.connect(host=db_definition['HOST'],
            port=int(db_definition['PORT']),
            user=db_definition['USER'],
            passwd=db_definition['PASSWORD'],
            db=db_definition['NAME'])
        db.close()
        return True
    except Exception as e:
        print('Database down:',database_name)
        return False

class dbRouter:
    def db_for_read(self, model, **hints):
        dblist = ['default', 'node02', 'node03']
        choice = random.choice(dblist)
        while not dbUp(choice):
            dblist.remove(choice)
            choice = random.choice(dblist)
            if len(dblist) == 1:
                break
        return choice

    def db_for_write(self, model, **hints):
        dblist = ['default', 'node02', 'node03']
        choice = random.choice(dblist)
        while not dbUp(choice):
            dblist.remove(choice)
            choice = random.choice(dblist)
            if len(dblist) == 1:
                break
        #return choice
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {'default', 'node02', 'node03'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
