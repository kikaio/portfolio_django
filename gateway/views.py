from django.shortcuts import render
# Create your views here.

TEMPLATE_ROOT = 'gateway'


def render_gateway(request, templates_name:str='', context:dict= {}):
    return render(request, f'{TEMPLATE_ROOT}/{templates_name}', context)


def index(req):
    return render_gateway(req, 'index.html')