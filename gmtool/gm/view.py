
from django.shortcuts import render

TEMPLATE_ROOT = 'gmtool/gm'

def render_gm(req, template_name:str='', context:dict={}):
    return render(req, f'{TEMPLATE_ROOT}/{template_name}')


def gm_login(req):
    return render_gm(req, 'login.html')

def gm_register(req):
    return render_gm(req, 'register.html')

def gm_change_pw(req):
    return render_gm(req, 'change_password.html')

def gm_reset_pw(req):
    return render_gm(req, 'forgot_password.html')