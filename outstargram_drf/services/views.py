from django.shortcuts import render

from rest_framework import generics


from outstargram_drf.services.models import *
from outstargram_drf.services.serializer import *
# Create your views here.

class PostListGeneric(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = SerPost
    pass

class PostDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = SerPost
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

