from gmtool.oauth.enum import *
from django.db import models

class GmPlatform(models.Model):
    """
    OAuth 고려한 Gm 추가 정보를 저장.
    """
    gm = models.ForeignKey(
        'Gm',
        on_delete=models.CASCADE,
        related_name='Platform',
        related_query_name='platform',
        blank=False,
    )
    platform_type = models.IntegerField(
        default=PlatformType.NONE,
        choices=PlatformType.ToChoices(),
        null=True,
        blank=False,
    )

    access_token = models.CharField(
        default='',
        null=True,
        blank=True,
        max_length=100,
    )

    reflesh_token = models.CharField(
        default='',
        null=True,
        blank=True,
        max_length=100,
    )

    auth_state = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )

    pass