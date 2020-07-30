from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators

from datetime import datetime


User = get_user_model()

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    follower_cnt = models.IntegerField(default=0)
    follow_cnt = models.IntegerField(default=0)
    desc = models.CharField(
        default='',
        max_length= 100,
        blank=True,
        null=False
    )


class Post(models.Model):
    """작성글"""
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, default=None)
    contents = models.CharField(max_length=150)
    date_registed = models.DateTimeField(default=datetime.utcnow)
    like_cnt = models.IntegerField(default=0, validators=[
      validators.MinValueValidator(1),
    ])
    class Meta:
        ordering=['date_registed']

    # followers = models.ManyToManyRel('self', related_name='followees', related_query_name='followee', symmetrical=False)
    pass


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contents = models.CharField(max_length=100, default='')
    date_registed = models.DateTimeField(default=datetime.utcnow)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __srt__(self):
        return f'{self.author}:{self.contents}'

class Photo(models.Model):
    post = models.ForeignKey(Post, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to='out_photos',
        default='media/default_img.jpg',
        null=True,
        blank=True
    )
    pass


class FollowRelation(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='followee', on_delete=models.CASCADE)
    pass


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_user = models.ForeignKey(User, on_delete=models.CASCADE)
    pass


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like_user = models.ForeignKey(User, on_delete=models.CASCADE)
    pass

