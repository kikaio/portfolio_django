from django.shortcuts import render
from django.conf import settings
from django.utils.translation import gettext as _
# Create your views here.

TEMPLATE_ROOT = 'gateway'

static_img_path = getattr(settings, 'STATIC_ROOT', 'static/') + 'gateway/img'

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
    return render_gateway(req, 'contact.html')