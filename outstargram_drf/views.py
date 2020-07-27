
from django.shortcuts import render

from rest_framework.reverse import reverse

from outstargram_drf.sign.views import *
from outstargram_drf.services.views import *

# Create your views here.

@api_view(['GET'])
def index(req, format=None):
    context = {}
    context['gm_list'] = reverse(
        'outstargram-drf:gm-list',
        request=req,
        format = format
    )
    context['author_list'] = reverse(
        'outstargram-drf:author-list',
        request=req,
        format=format
    )
    return Response(context)
