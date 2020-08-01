from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins


from outstargram_drf.services.models import *
from outstargram_drf.services.serializer import *
# Create your views here.

class PostListPager(PageNumberPagination):
    page_size = 2
    max_page_size = 100
    page_size_query_param = 'page_size'


class PostListGeneric(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = SerPost
    pagination_class = PostListPager

    permission_classes = [
        permissions.IsAuthenticated,
        IsPostOwnerOrReadOnly,
    ]

    def get_queryset(self):
        target_id = self.request.query_params.get('author',  None)
        if target_id is None:
            return Post.objects.all()
        else:
            return Post.objects.filter(user=target_id)
    pass

class PostDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = SerPost

    permission_classes = [
        IsPostOwnerOrReadOnly,
    ]

    pass


class PhotoListGeneric(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = SerPhoto

    def get_queryset(self):
        target_id = self.request.query_params.get('post', None)
        if not target_id:
            return Photo.objects.all()
        else:
            return Photo.objects.filter(post=target_id)
    pass


class PhotoDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = SerPhoto
    pass


class CommentListGeneric(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = SerComment

    def get_queryset(self):
        target_id = self.request.query_params.get('post', None)
        if not target_id:
            return Comment.objects.all()
        else:
            return Comment.objects.filter(post=target_id)
        pass

    pass


class CommentDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = SerComment
    pass


class FollowRelationGeneric(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    queryset = FollowRelation.objects.all()
    serializer_class = SerFollowRelation

    def get_queryset(self):
        user_id = self.request.query_params.get('followee',  None)
        if not user_id:
            return FollowRelation.objects.all()
        else:
            return FollowRelation.objects.filter(followee__exact = user_id)
        pass

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)

    pass


class PostLikeGeneric(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    """사진 좋아요"""
    queryset = PostLike.objects.all()
    serializer_class = SerPostLike
    pass


class CommentLikeGeneric(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    queryset = CommentLike.objects.all()
    serializer_class = SerCommentLike

