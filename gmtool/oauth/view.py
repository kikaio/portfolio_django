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


def regist_or_login_platform(req, user_email, access_token, validate_sec, platform_type = PlatformType.NONE):
    if platform_type == PlatformType.NONE:
        return None

    user = None
    platform_data = None
    if not User.objects.filter(email__exact = user_email).exists():
        print(f'email : platform-{platform_type.name} user-{user_email} created')
        user = User.objects.create_user(user_email, access_token)
        if user is not None:
            platform_data = GmPlatform(gm=user, platform_type = platform_type, access_token = access_token)
            platform_data.save()
            pass
        pass
    else:
        user = User.objects.get(email=user_email)
        # 기존 oauth 로그인을 한 유저.
        if user.Platform.exists():
            platform = user.Platform.first()
            # 타 플랫폼으로 이미 계정 연동 -> error.
            if platform.platform_type != platform_type:
                print(f'email : user-{user_email} has already logined platform-{platform.platform_type.name}')
                return None
            platform.access_token = access_token
            platform.save()
            user.set_password(access_token)
            user.save()
            print(f'email : user-{user_email} logined platform-{platform.platform_type.name}')
        else:
            print(f'email : user-{user_email} has created account using this mail')
            # 이미 해당 email을 사용한 일반 로그인이 존재하는 경우. 별도 view 추가할 예정.
            return redirect(reverse('gmtool:index'))

    if authenticate(req, email = user_email, password = access_token):
        # 세션 timeout도 validate_sec으로 지정.
        req.session.set_expiry(validate_sec)
        login(req, user)
        return redirect(reverse('gmtool:index'))

    pass


def oauth_login(req):
    context = {}
    context['facebook'] = True
    context['google'] = True
    return render_oauth(req, 'oauth_login.html', context)

"""
Facebook OAuth 2
"""

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

    ret_token_data = get_token_data_facebook(auth_setting, redirect_uri, code)
    access_token = ret_token_data['access_token']
    validate_sec = ret_token_data['expires_in']

    if not is_valid_access_token_facebook(auth_setting['CLIENT_ID'], auth_setting['CLIENT_SECRET'], access_token):
        pass

    user_data = get_user_data_facebook(access_token)

    user_email = user_data['email']

    regist_or_login_platform(req, user_email, access_token, validate_sec, PlatformType.FACE_BOOK)

    return redirect(reverse('gmtool:index'))
    pass

def get_token_data_facebook(auth_setting, redirect_uri, code):
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

def is_valid_access_token_facebook(client_id, client_secret, access_token):
    "access_token의 유효성 검사."
    params = {
        'input_token':access_token,
        'access_token' : f'{client_id}|{client_secret}'
    }
    check_url = 'https://graph.facebook.com/debug_token'

    ret = requests.get(check_url, params=params)
    return ret.json()['data']['is_valid']

def get_user_data_facebook(access_token):
    "user 관련 data 획득, 필요한 data는 field에 추가."
    need_data = ['email']
    get_url = 'https://graph.facebook.com/me'
    params = {
        'fields': ','.join(need_data),
        'access_token' : access_token
    }

    ret = requests.get(get_url, params = params)
    return ret.json()

def app_cancel_facebook(req):
    if not req.method == 'POST':
        return redirect(reverse('gmtool:err-400'))
    post_data = req.POST
    print(post_data)



"""
Google OAuth2 
"""

def oauth_login_google(req):
    oauth_setting = getattr(settings, 'GOOGLE', None)
    if oauth_setting is None:
        pass
    view_name = oauth_setting["REDIRECT_URL_NAME"]
    cur_url = reverse(f'gmtool:{view_name}')
    host = req.get_host()
    if host == '127.0.0.1:8000':
        host = 'localhost:8000'
    redirect_url =f'http://{host}{cur_url}'

    google_auth_uri = oauth_setting["AUTH_URI"]
    client_id = oauth_setting["CLIENT_ID"]

    params = {
        "client_id" : client_id,
        "redirect_uri" : redirect_url,
        "response_type" : "code",
        "scope" : "email",
    }
    to = f'{google_auth_uri}?'
    for key, value in params.items():
        to += f'{key}={value}&'

    # return redirect(google_auth_uri, params)
    return redirect(to)


def oauth_redirect_google(req):
    get_data = req.GET
    print(get_data)

    # error page 추가할 것.
    if get_data.get('error', None) is not None:
        pass


    code = get_data.get('code', None)
    scope = get_data.get('scope', None)

    oauth_setting = getattr(settings, 'GOOGLE', None)
    view_name = oauth_setting["REDIRECT_URL_NAME"]
    cur_url = reverse(f'gmtool:{view_name}')
    host = req.get_host()
    if host == '127.0.0.1:8000':
        host = 'localhost:8000'
    redirect_uri =f'http://{host}{cur_url}'

    token_data = get_token_data_google(oauth_setting, code, redirect_uri)
    print(f'token_data : {token_data}')
    # error page 추가할 것.
    if token_data.get('error', None) is not None:
        pass

    id_token = get_decoded_id_token_google(oauth_setting, token_data)

    regist_or_login_platform(req, id_token['email'], token_data['access_token'], token_data['expires_in'], PlatformType.GOOGLE)

    return redirect(reverse('gmtool:index'))


def get_token_data_google(oauth_setting, code, redirect_url):
    client_id = oauth_setting["CLIENT_ID"]
    client_secret = oauth_setting["CLIENT_SECRET"]

    token_uri = oauth_setting['TOKEN_URI']
    params = {
        'code': code,
        'client_id' : client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_url,
        'grant_type': 'authorization_code',
    }
    ret = requests.post(token_uri, params = params)
    return ret.json()


def get_decoded_id_token_google(oauth_setting, token_data):
    import jwt
    from jwt.algorithms import RSAAlgorithm
    "해당 id_token은 json web token으로 디코딩 해야함. -> PyJwt,  pyjwt[crypto], cryptography install 필수."
    id_token = f'{token_data.get("id_token", None)}'
    if id_token is not None:
        "해당 token에 대한 검증 절차. https://www.ykrods.net/posts/2019/04/30/pyjwt-id_token-validation/ -> 참고."
        cert_uri = 'https://www.googleapis.com/oauth2/v3/certs'
        jwt_header = jwt.get_unverified_header(id_token)
        ret_keys = requests.get(cert_uri).json()['keys']
        cur_key = None
        for jwt_key in ret_keys :
            if jwt_key['kid'] == jwt_header['kid']:
                cur_key = jwt_key
                break
        if cur_key is None:
            return None
        public_key = RSAAlgorithm.from_jwk(json.dumps(cur_key))
        id_token = jwt.decode(id_token, public_key, issure = 'https://accounts.google.com', audience=oauth_setting['CLIENT_ID'], algorithms=['RS256'])
    return id_token
