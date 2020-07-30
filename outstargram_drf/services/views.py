from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

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

    def get_queryset(self):
        author_id = self.request.query_params.get('author',  None)
        if author_id is None:
            return Post.objects.all()
        else:
            return Post.objects.filter(author__exact=int(author_id))
    pass

class PostDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = SerPost
    pass


class PhotoListGeneric(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = SerPhoto
    pass

class CommentListGeneric(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = SerComment
    pass


def follow(req, target):
    """해당 유저 팔로우"""
    pass

def unfollow(req, target):
    """해당 유저 언팔로우"""
    pass

def post_upload(req):
    """사진 업로드"""
    pass

def post_like(req, post_id):
    """사진 좋아요"""
    pass

def post_like_cancel(req, post_id):
    """사진 좋아요 취소"""
    pass

def post_delete(req, post_id):
    """포스트 삭제"""
    pass

def post_comment(req, post_id):
    """댓글"""
    pass

def post_comment_delete(req, comment_id):
    """댓글 삭제"""
    pass

def post_comment_like(req, comment_id):
    """댓글 좋아요"""
    pass

def post_commnet_like_cancel(req, commnet_id):
    """댓글 좋아요 취소"""
    pass

def post_comment_reply(req, comment_id):
    """대댓글"""
    pass


def search(req, text):
    pass

