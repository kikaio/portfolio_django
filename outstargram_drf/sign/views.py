from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework import mixins
from rest_framework import generics

from outstargram_drf.sign.serializer import *
from outstargram_drf.services.serializer import *


@api_view(['GET', 'POST'])
def gm_list(req, format=None):
    if req.method == 'POST':
        data = JSONParser().parse(req)
        ser = SerGm(data = data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    elif req.method == 'GET':
        gms = get_list_or_404(User)
        for ele in gms:
            if not ele.author.exists():
                author = Author()
                author.user = ele
                author.save()
        ser = SerGm(gms, many=True)
        return Response(ser.data)

class GmListAPI(APIView):

    def get(self, req, format=None):
        gms = get_list_or_404(User)
        ser = SerGm(gms, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def post(self, req, format=None):
        ser = SerGm(data = req.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
pass


class GmListMixin(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SerGm

    def get(self, req, *args, **kwargs):
        return self.list(req, *args, **kwargs)

    def post(self, req, *args, **kwargs):
        return self.create(req, *args, **kwargs)
    pass


class GmListGeneric(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = SerGm
    pass


@api_view(['GET', 'PUT', 'DELETE'])
def gm_detail(req, pk, format=None):
    ser = None
    gm = get_object_or_404(User, pk)
    if req.method =='GET':
        ser = SerGm(ser)
        return Response(ser.data)
    elif req.method =='PUT':
        data = JSONParser().parse(req)
        ser = SerGm(gm, data = data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    elif req.method =='DELETE':
        User.objects.delete(id=pk)
        return Response(status.HTTP_204_NO_CONTENT)
    pass

class GmDetailAPI(APIView):

    def get(self, req, pk, format=None):
        gm = get_object_or_404(User, pk)
        ser = SerGm(gm)
        return Response(ser.data)

    def put(self, req, pk, format=None):
        gm = get_object_or_404(User, pk)
        ser = SerGm(gm, data=req.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, pk, format=None):
        gm = get_object_or_404(User, pk)
        gm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    pass


class GmDetailMixin(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = SerGm

    def get(self, req, *args, **kwargs):
        return self.retrieve(req, *args, **kwargs)

    def put(self, req, *args, **kwargs):
        return self.update(req, *args,**kwargs)

    def delete(self, req, *args, **kwargs):
        return self.destroy(req, *args, **kwargs)

    pass


class GmDetailGeneric(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = SerGm
    pass

@api_view(['GET', 'POST'])
def author_list(req, format=None):
    if req.method == 'POST':
        data = JSONParser().parse(req)
        ser = SerAuthor(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    elif req.method == 'GET':
        authors = get_list_or_404(Author)
        ser = SerAuthor(authors, many=True)
        return Response(ser.data)
    pass


class AuthorListAPI(APIView):

    def get(self, req, format=None):
        authors = get_list_or_404(Author)
        ser = SerAuthor(authors, many=True)
        return Response(ser.data)

    def post(self, req, format=None):
        ser = SerAuthor(data = req.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    pass


class AuthorListMinxin(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):

    queryset = Author.objects.all()
    serializer_class = SerAuthor

    def get(self, req, *args, **kwargs):
        return self.list(req, *args, **kwargs)

    def post(self, req, *args, **kwargs):
        return self.create(req, *args, **kwargs)
    pass


class AuthorListGeneric(generics.ListCreateAPIView):

    queryset = Author.objects.all()
    serializer_class = SerAuthor
    pass


@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(req, pk, format=None):
    ser = None
    author = get_object_or_404(Author, pk)
    if req.method =='GET':
        ser = SerAuthor(author)
        return Response(ser.data)
    elif req.method == 'PUT':
        data = JSONParser().parse(req)
        ser = SerAuthor(author, data=data)
        if ser.is_valid():
            ser.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    elif req.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    pass


class AuthorDetailAPI(APIView):

    def get(self, req, pk, format=None):
        author = get_object_or_404(Author, pk)
        ser = SerAuthor(author)
        return Response(ser.data)

    def put(self, req, pk, format=None):
        author = get_object_or_404(Author, pk)
        ser = SerAuthor(author, data = req.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, pk, format=None):
        author = get_object_or_404(Author, pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    pass


class AuthorDetailMixin(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):

    def get(self, req, *args, **kwargs):
        return self.retrieve(req, *args, **kwargs)

    def put(self, req, *args, **kwargs):
        return self.update(req, *args, **kwargs)

    def delete(self, req, *args, **kwargs):
        return self.destroy(req, *args, **kwargs)

    pass


class AuthorDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = SerAuthor
    pass