import random

class dbRouter:
    def db_for_read(self, model, **hints):
        return random.choice(['default', 'node02', 'node03'])

    def db_for_write(self, model, **hints):
        return random.choice(['default', 'node02', 'node03'])

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {'default', 'node02', 'node03'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
