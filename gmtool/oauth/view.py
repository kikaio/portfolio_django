from django.views import generic
from django.shortcuts import render, redirect, reverse


OAUTH_ROOT = 'gmtool/oauth'

def render_oauth(req, template_name:str='', context:dict={}):
    return render(req, f'{OAUTH_ROOT}/{template_name}', context)


def oauth_login(req):
    return render_oauth(req, 'oauth_login.html')
