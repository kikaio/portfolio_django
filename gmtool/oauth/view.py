from django.views import generic
from django.shortcuts import render, redirect, reverse
from django.conf import settings
import requests

import json


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
    cur_url = reverse('gmtool:index')+auth_setting["REDIRECT_URL_NAME"]
    redirect_uri = f"https://{req.get_host()}{cur_url}"
    # uri = https://127.0.0.1:8000/gmtool/oauth-redirect-facebook
    # 위변조 확인용.
    cur_oauth_state = auth_setting['SECRET']

    login_req_url = 'https://www.facebook.com/v7.0/dialog/oauth'
    ret = f'{login_req_url}?client_id={client_id}&redirect_uri={redirect_uri}&state={cur_oauth_state}'
    # response_type을 명시하지 않는경우 default로 code 값이 응답에 포함됨.
    print(ret)
    return redirect(ret)
pass

def oauth_redirect_facebook(req):
    """
    :param req:
    :return:
    """
    print(req)
    get_data = req.GET
    err_reason = get_data.get('err_reason', None)
    # user가 facebook login을 하지 않은 경우
    if err_reason is not None:
        error = get_data.get('error', None)
        error_description = get_data.get('error_description', None)
        pass
    # for ele in get_data:
    #     print(f'{ele.key} : {ele.value}')
    code = get_data.get('code', None)
    if code is None:
        pass
    auth_setting = getattr(settings, 'FACEBOOK', None)
    if auth_setting is None:
        return None
    client_id = auth_setting['CLIENT_ID']
    client_secret = auth_setting['CLIENT_SECRET']
    cur_url = reverse('gmtool:index') + auth_setting["REDIRECT_URL_NAME"]
    redirect_uri = f"https://{req.get_host()}{cur_url}"
    get_token_url = 'https://graph.facebook.com/v7.0/oauth/access_token'
    params = {
        'client_id' : client_id,
        'redirect_uri' : redirect_uri,
        'client_secret' : client_secret,
        'code' : code
    }
    reply = requests.get(get_token_url, params=params)

    print(f'oauth_code_facebook:{reply.json()}')
    return redirect(reverse('gmtool:index'))
    pass

def oauth_expired_facebook(req):
    return redirect(reverse('gmtool:index'))
