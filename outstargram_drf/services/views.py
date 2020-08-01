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
        # permissions.IsAuthenticated,
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

    permission_classes = [
        IsDeleteJustForUser,
    ]

    pass


class FollowRelationListGeneric(generics.ListCreateAPIView):
    queryset = FollowRelation.objects.all()
    serializer_class = SerFollowRelation

    def get_queryset(self):
        user_id = self.request.query_params.get('id',  None)
        is_followee = self.request.query_params.get('is_followee', None)
        if not user_id:
            return FollowRelation.objects.all()
        else:
            if not is_followee or (bool(is_followee) is False):
                return FollowRelation.objects.filter(follower=user_id)
            else:
                return FollowRelation.objects.filter(followee=user_id)
        pass

    pass


class FollowRelationDetailGeneric(mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin,
                                  generics.GenericAPIView):
    queryset = FollowRelation.objects.all()
    serializer_class = SerFollowRelation

    permission_classes = [
        IsFollowerCancel,
    ]

    def get(self, req, *args, **kwargs):
        return self.retrieve(req, *args, **kwargs)

    def delete(self, req, *args, **kwargs):
        return self.destroy(req, *args, **kwargs)

    pass


class PostLikeListGeneric(generics.ListCreateAPIView):
    """사진 좋아요 목록"""
    queryset = PostLike.objects.all()
    serializer_class = SerPostLike

    def get_queryset(self):
        target_id = self.request.query_params.get('post', None)
        if target_id is None:
            return PostLike.objects.all()
        else:
            return PostLike.objects.filter(post__exact=target_id)
    pass


class PostLikeDetailGeneric(mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    queryset = PostLike.objects.all()
    serializer_class = SerPostLike

    permission_classes = [
        IsJustForUserLikeCancel,
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    pass


class CommentLikeListGeneric(generics.ListCreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = SerCommentLike

    def get_queryset(self):
        target_id = self.request.query_params.get('comment', None)
        if target_id is None:
            return CommentLike.objects.all()
        else:
            return CommentLike.objects.filter(comment__exact=target_id)
    pass

class CommentLikeDetailGeneric(mixins.RetrieveModelMixin,
                               mixins.DestroyModelMixin,
                               generics.GenericAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = SerCommentLike
    permission_classes = [
        IsJustForUserLikeCancel,
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    pass