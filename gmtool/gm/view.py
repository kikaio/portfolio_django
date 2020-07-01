
from django.shortcuts import render, reverse
from gmtool.gm.form import *
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
TEMPLATE_ROOT = 'gmtool/gm'

def render_gm(req, template_name:str='', context:dict={}):
    return render(req, f'{TEMPLATE_ROOT}/{template_name}', context)

@login_required
def gm_logout(req):
    logout(req)
    return redirect(reverse('gmtool:index'))

def gm_login(req):
    context = {}
    form =None
    if req.method == 'POST':
        form = GmLoginForm(req.POST)
        if form.is_valid():
            # 실제로 내부에선 로그인 처리.
            if form.login(req):
                return redirect(reverse('gmtool:index'))
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

@login_required
def gm_change_pw(req):
    form = None
    context = {}
    if req.method =='POST':
        form = GmChangePwForm(req.POST, request=req)
        if form.is_valid():
            form.save(req)
            return redirect(reverse('gmtool:index'))
    elif req.method=='GET':
        form = GmChangePwForm(request=req)

    context['form'] = form
    return render_gm(req, 'change_password.html', context)

def gm_reset_pw(req):
    form = None
    context = {}
    context['reset'] = True
    if req.method=='POST':
        form = GmPwResetForm(req.POST)
        if form.is_valid():
            form.send_reset_mail(req)
            # 메일 전송 완료 template로 redirect
            print('aaa')
            return redirect(reverse(form.template_name_req))
    elif req.method=='GET':
        form = GmPwResetForm()

    context['form'] = form
    return render_gm(req, 'forgot_password.html', context)

def gm_reset_pw_req(req):
    context = {}
    context['reset_req'] = True
    "reset 요청 후 보여주는 단순 page"
    return render_gm(req, 'forgot_password.html', context)

def gm_reset_pw_token(req, uidb64, token):
    from django.contrib.auth.views import PasswordResetConfirmView
    context = {}
    form = None
    if req.method=='POST':
        form = GmPwTokenForm(request=req, uid=uidb64, token=token)
        if form.is_valid():
            print('is valid?')
            if form.check_token():
                print('checked token')
                return redirect(reverse(form.template_name_done))
    elif req.method == 'GET':
        form = GmPwTokenForm(req.POST, request=req, uid=uidb64, token=token)

    context['reset_token'] = True
    context['form'] = form
    return render_gm(req, 'forgot_password.html', context)

def gm_reset_pw_done(req):
    context = {}
    context['reset_done'] = True

    return render_gm(req, 'forgot_password.html', context)
