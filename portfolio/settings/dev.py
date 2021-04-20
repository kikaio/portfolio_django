from .base import *

sql_json = get_json_content('confs/db_dev.json')

DATABASES = {
    'default': {
        "ENGINE" : get_val_from_json(sql_json, 'engine'),
        "NAME" : get_val_from_json(sql_json, 'name'),
        "USER" : get_val_from_json(sql_json, 'user'),
        "PASSWORD": get_val_from_json(sql_json, 'pw'),
        "HOST" : get_val_from_json(sql_json, 'host'),
        "PORT" : get_val_from_json(sql_json, 'port'),
        "OPTIONS" : {
            'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}

WSGI_APPLICATION = 'portfolio.wsgi.debug.application'
