from django.views import generic
from django.shortcuts import render, redirect, reverse
from django.conf import settings

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
    auth_setting = getattr(settings, 'FACEBOOK', None)
    if auth_setting is None:
        return
    client_id = auth_setting['CLIENT_ID']

    host_url = reverse('gmtool:index')
    redirect_uri = f"{host_url}/{auth_setting['REDIRECT_URL_NAME']}"

    # 위변조 확인용.
    cur_oauth_state = auth_setting['SECRET']

    login_req_url = 'https://www.facebook.com/v7.0/dialog/oauth'
    ret = f'{login_req_url}?client_id={client_id}&redirect_uri={redirect_uri}&state={cur_oauth_state}'
    print(ret)
    return redirect(ret)
pass

def oauth_redirect_facebook(req, state):
    auth_setting = getattr(settings, 'FACEBOOK', None)
    if auth_setting is None:
        return redirect(reverse('gmtool:err-400'))
    origin_secret = auth_setting['SECRET']
    if origin_secret != state:
        return redirect(reverse('gmtool:err-400'))
    return
pass
