import requests
import json

from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model

from gmtool.oauth.enum import *
from gmtool.oauth.model import GmPlatform

User = get_user_model()

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
    ret = f'{login_req_url}?client_id={client_id}&redirect_uri={redirect_uri}&state={cur_oauth_state}&scope=email'
    # response_type을 명시하지 않는경우 default로 code 값이 응답에 포함됨.
    print(ret)
    return redirect(ret)

def oauth_redirect_facebook(req):
    """
    :param req:
    :return:
    """
    get_data = req.GET
    # user가 facebook login을 취소 경우
    if get_data.get('error', None) is not None:
        context = {
            'facebook' : True,
            'code' : get_data.get('error_code', None),
            'reason' : get_data.get('error_reason', None),
            'error' : get_data.get('error', None),
            'desc' : get_data.get('error_description', None),
        }
        return render_oauth(req, 'oauth_login_cancel.html', context)
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
    access_token = ret_token_data['access_token']
    validate_sec = ret_token_data['expires_in']

    if not is_valid_access_token(auth_setting['CLIENT_ID'], auth_setting['CLIENT_SECRET'], access_token):
        pass

    user_data = get_facebook_user_data(access_token)

    user_email = user_data['email']

    regist_or_login_facebook(req, user_email, access_token, validate_sec)

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
    return reply.json()

def is_valid_access_token(client_id, client_secret, access_token):
    "access_token의 유효성 검사."
    params = {
        'input_token':access_token,
        'access_token' : f'{client_id}|{client_secret}'
    }
    check_url = 'https://graph.facebook.com/debug_token'

    ret = requests.get(check_url, params=params)
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

def regist_or_login_facebook(req, user_email, access_token, validate_sec):
    user = None
    platform_data = None
    if not User.objects.filter(email__exact = user_email).exists():
        user = User.objects.create_user(user_email, access_token)
        if user is not None:
            platform_data = GmPlatform(gm=user, platform_type = PlatformType.FACE_BOOK, access_token = access_token)
            platform_data.save()
            pass
        pass
    else:
        user = User.objects.get(email=user_email)
        # 기존 oauth 로그인을 한 유저.
        if user.Platform.exists():
            platform = user.Platform.first()
            platform.access_token = access_token
            platform.save()
            user.set_password(access_token)
            user.save()
        else:
            # 이미 해당 email을 사용한 일반 로그인이 존재하는 경우. 별도 view 추가할 예정.
            return redirect(reverse('gmtool:login'))

    if authenticate(req, email = user_email, password = access_token):
        # 세션 timeout도 validate_sec으로 지정.
        req.session.set_expiry(validate_sec)
        login(req, user)
        return redirect(reverse('gmtool:index'))

    pass


def app_cancel_facebook(req):
    if not req.method == 'POST':
        return redirect(reverse('gmtool:err-400'))
    post_data = req.POST
    print(post_data)
