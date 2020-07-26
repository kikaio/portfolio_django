from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
User = get_user_model()

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower_Cnt = models.IntegerField(default=0)
    follow_cnt = models.IntegerField(default=0)
    desc = models.CharField(
        default='',
        max_length= 100,
        blank=True,
        null=False
    )

class Post(models.Model):
    """작성글"""
    contents = models.CharField(max_length=150)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_registed = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        ordering=['date_registed']

    # followers = models.ManyToManyRel('self', related_name='followees', related_query_name='followee', symmetrical=False)
    pass
#
# class Comment(models.Model):
#     """post에 대한 댓글, 또는 그에 대한 대댓글"""
#     post = models.ForeignKey(Post)
#     user = models.ForeignKey(User)
#     contents = models.CharField(max_length=100)
#     for_reply = models.IntegerField(default=None, null=True, blank=True)
#     pass
#