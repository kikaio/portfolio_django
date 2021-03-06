from django.shortcuts import render

from gmtool.gm.view import *
from gmtool.manage.view import *
from gmtool.log.view import *
from gmtool.files.view import *
from gmtool.oauth.view import *
from gmtool.err.view import *


# Create your views here.

TEMPLATE_ROOT = 'gmtool'

def redner_gmtool(req, template_name:str='', context:dict = {}):
    return render(req, f'{TEMPLATE_ROOT}/{template_name}', context)


def index(req):
    return redner_gmtool(req, 'index.html', {})
