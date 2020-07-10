from django.views import generic
from django.shortcuts import render, redirect, reverse
from django.conf import settings

from gmtool.oauth.enum import AuthState


OAUTH_ROOT = 'gmtool/oauth'


def render_oauth(req, template_name:str='', context:dict={}):
    return render(req, f'{OAUTH_ROOT}/{template_name}', context)


def oauth_login(req):
    context = {}
    facebook = {
        'client_id':'',
        'redirect_url':'',

    }
    context['facebook'] =facebook
    return render_oauth(req, 'oauth_login.html', context)
pass

def oauth_login_facebook(req):
    """
     facebook-OAuth2 용 로그인
    """
    auth_setting = settings.configure('FACEBOOK', None)
    if auth_setting is None:
        return
    client_id = auth_setting['CLIENT_ID']
    redirect_url = auth_setting['REDIRECT_URL']
    cur_oauth_state = AuthState.LOGIN_REQ
    login_req_url = 'https://www.facebook.com/v7.0/dialog/oauth'
    return redirect(f'{login_req_url}?{client_id}&{redirect_url}&{cur_oauth_state}')

pass