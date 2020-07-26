from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from outstargram_drf.sign.serializer import *
from outstargram_drf.services.serializer import *


@csrf_exempt
def gm_list(req):
    if req.method == 'POST':
        data = JSONParser().parse(req)
        ser = SerGm(data = data)
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status=201)
        return JsonResponse(ser.errors, status=400)
    elif req.method == 'GET':
        gms = User.objects.all()
        ser = SerGm(gms, many=True)
        return JsonResponse(ser.data, safe = False)

def gm_detail(req, pk):
    pass

@csrf_exempt
def author_list(req):
    if req.method == 'POST':
        pass
    elif req.method == 'GET':
        pass
    else:
        pass
    pass