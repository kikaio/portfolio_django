import os
import sys

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

path = '/home/kikaio/'  # PythonAnywhere 계정으로 바꾸세요.
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'portfolio.settings.pythonanywhere'

application = StaticFilesHandler(get_wsgi_application())