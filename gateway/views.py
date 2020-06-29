from django.shortcuts import render
from django.conf import settings
from django.utils.translation import gettext as _

from gateway.forms import *
from django.core.mail import EmailMessage
# Create your views here.

TEMPLATE_ROOT = 'gateway'

static_img_path = getattr(settings, 'STATIC_ROOT', 'static/') + 'gateway/img'
developer_mail = getattr(settings, 'DEVELOPER_MAIL', 'gjduddnr5923@gmail.com')


def render_gateway(request, templates_name:str='', context:dict= {}):
    return render(request, f'{TEMPLATE_ROOT}/{templates_name}', context)


def index(req):

    app_list = []
    # template에서 간편하게 사용하기 위해 list형으로 활용할 것.
    # icon_path, app_name, desc, reverse_name 순서.
    app_list.append([
        f'{static_img_path}/icon_gmtool.png',
        'gmtool',
        _('This App is first portfolio about tool for gm users'),
        'gmtool:index',
    ])
    app_list.append([
        f'{static_img_path}/icon_commingsoon.png',
        _('This App is comming soon'),
        'commingsoon',
        'gateway:index',
    ])

    return render_gateway(req, 'index.html', {'apps' : app_list})


def contact(req):
    if req.method == 'GET':
        form = ContactForm()
        return render_gateway(req, 'contact.html', {'form':form})
    elif req.method == 'POST':
        form = ContactForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name', 'Something is wrong')
            email = form.cleaned_data.get('email', 'Something is wrong')
            msg_body = form.cleaned_data.get('msg_body', 'Something is wrong')
            try:
                send_contact_mail(name, email, msg_body)
                return render_gateway(req, 'send_email_complete.html', {'form': form})
            except:
                pass
        else:
            pass
    return render_gateway(req, 'contact.html')


def send_contact_mail(name, email, msg):
    print(f'name : {name} mail : {email} msg : {msg}, -> to {developer_mail}')
    subject = f'Contact Request mail from {name}[portfolio]'
    body = msg
    from_email = email

    msg = EmailMessage(subject = subject, body=body, from_email=from_email, to=[developer_mail, ])
    msg.send()
    pass
