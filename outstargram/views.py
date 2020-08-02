from django.shortcuts import render, reverse, redirect

# Create your views here.


TEMPLATE_ROOT = 'outstargram'
def outstargram_render(req, template_name:str='', context:dict={}):
    return render(req, f'{TEMPLATE_ROOT}/{template_name}', context)


def index(req):
    return outstargram_render(req, 'index.html')

