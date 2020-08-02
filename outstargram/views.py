from django.shortcuts import render, reverse, redirect
import requests

# Create your views here.


TEMPLATE_ROOT = 'outstargram'
def outstargram_render(req, template_name:str='', context:dict={}):
    return render(req, f'{TEMPLATE_ROOT}/{template_name}', context)

def get_drf_response(req, method_name:str, url_name:str, *args, **kwargs):
    drf_host = req.get_host()
    if method_name.lower() == 'get':
        return requests.get(f"http://{drf_host}{reverse(f'outstargram-drf:{url_name}', *args, **kwargs)}.json")
    elif method_name.lower() == 'post':
        return requests.post(reverse(f'outstargram-drf:{url_name}', *args, **kwargs))
    elif method_name.lower() == 'put':
        return requests.put(reverse(f'outstargram-drf:{url_name}', *args, **kwargs))
    elif method_name.lower() == 'delete':
        return requests.delete(reverse(f'outstargram-drf:{url_name}', *args, **kwargs))
    return None


def index(req):
    return outstargram_render(req, 'index.html')

def test(req):
    res = get_drf_response(req, 'get', 'post-list')
    print(res.text)
    return outstargram_render(req, 'index.html', {'res':res})