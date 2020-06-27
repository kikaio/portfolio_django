from django.shortcuts import render

# Create your views here.

TEMPLATE_ROOT = 'blog'

def redner_gmtool(req, template_name:str='', context:dict = {}):
    return render(req, f'{TEMPLATE_ROOT}/{template_name}', context)


def index(req):
    return redner_gmtool(req, 'index.html', {})
