from .base import *

DEBUG = False

sql_json = get_json_content('confs/db_live.json')

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

WSGI_APPLICATION = 'portfolio.wsgi.live.application'


s3_json = get_json_content('aws_s3_key.json')


STATICFILES_STORAGE = 'aws.storage.StaticStorage'
STATICFILES_LOCATION = 'static'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'aws.storage.StaticStorage'



AWS_ACCESS_KEY_ID = get_val_from_json(s3_json, 'AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = get_val_from_json(s3_json, 'AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME  = get_val_from_json(s3_json, 'AWS_STORAGE_BUCKET_NAME')
AWS_REGION = get_val_from_json(s3_json, 'AWS_REGION')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME }.s3.{AWS_REGION}.amazonaws.com.'