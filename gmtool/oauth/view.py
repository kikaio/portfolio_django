from unittest.mock import _patch

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
    cur_url = reverse('gmtool:index') + auth_setting["REDIRECT_URL_NAME"]
    redirect_uri = f"https://{req.get_host()}{cur_url}"
    ret_token_data = get_token_data(auth_setting, redirect_uri, code)

    if not is_valid_access_token(auth_setting, ret_token_data['ret_token_data']):
        pass

    user_data = get_facebook_user_data(ret_token_data['ret_token_data'])

    user_email = user_data['email']
    


    return redirect(reverse('gmtool:index'))
    pass

def get_token_data(auth_setting, redirect_uri, code):
    "accewss_token 관련 정보를 json형식으로 받아옴. { access_token, token_type, expires_in:유효 시간{초} ]"
    client_id = auth_setting['CLIENT_ID']
    client_secret = auth_setting['CLIENT_SECRET']
    get_token_url = 'https://graph.facebook.com/v7.0/oauth/access_token'
    params = {
        'client_id' : client_id,
        'redirect_uri' : redirect_uri,
        'client_secret' : client_secret,
        'code' : code
    }
    reply = requests.get(get_token_url, params=params)

    print(f'oauth_code_facebook:{reply.json()}')
    return reply.json()

def is_valid_access_token(client_id, client_secret, access_token):
    "access_token의 유효성 검사."
    params = {
        'input_token':access_token,
        'access_token' : {client_id|client_secret}
    }
    check_url = 'graph.facebook.com/debug_token'

    ret = requests.get(check_url, params=params)
    print(f'is_valid_access_token:{ret.json()}')
    return ret.json()['data']['is_valid']

def get_facebook_user_data(access_token):
    "user 관련 data 획득, 필요한 data는 field에 추가."
    need_data = ['email']
    get_url = 'https://graph.facebook.com/me'
    params = {
        'fields': ','.join(need_data),
        'access_token' : access_token
    }

    ret = requests.get(get_url, params = params)
    return ret.json()




def oauth_expired_facebook(req):
    return redirect(reverse('gmtool:index'))
