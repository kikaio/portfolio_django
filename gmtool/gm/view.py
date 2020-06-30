
from django.shortcuts import render, reverse
from gmtool.gm.form import *


TEMPLATE_ROOT = 'gmtool/gm'

def render_gm(req, template_name:str='', context:dict={}):
    return render(req, f'{TEMPLATE_ROOT}/{template_name}', context)


def gm_login(req):
    context = {}
    form =None
    if req.method == 'POST':
        form = GmLoginForm(req.POST)
        if form.is_valid():
            # 실제로 내부에선 로그인 처리.
            if form.login(req):
                return render(req, 'gmtool/index.html')
            else:
                return render_gm(req, 'login_failed.html')
    elif req.method=='GET':
        form = GmLoginForm()

    context['form'] = form
    return render_gm(req, 'login.html', context)

def gm_register(req):
    form = None
    context = {}
    if req.method == 'POST':
        form = GmRegistForm(req.POST)
        if form.is_valid():
            form.save()
            context['next'] = reverse('gmtool:gm-login')
    elif req.method == 'GET':
        form = GmRegistForm()
        context['form'] = form
    return render_gm(req, 'register.html', context)

def gm_change_pw(req):
    return render_gm(req, 'change_password.html')

def gm_reset_pw(req):
    return render_gm(req, 'forgot_password.html')