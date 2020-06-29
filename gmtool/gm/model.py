
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.db import models
from django.utils.translation import gettext as _



class GmManager(BaseUserManager):

    def create_user(self, email, password = None, is_superuser = False):
        """
            gmtool 에서 사용할 user account를 생성.
        :param email: 각 gm별 개인 email
        :param password: password
        :return: user 객체
        """
        if email is None:
            raise ValueError(_('User must have an email address'))

        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.is_superuser = is_superuser
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password):
        """
            super user를 생성
        :param email: 계정 email
        :param password: 계정 비밀번호
        :return: is_superuser:true 인 user
        """
        user = self.create_user(email, password, is_superuser=True)
        return user

    pass


class Gm(AbstractBaseUser, PermissionsMixin):
    """
        기존 Account 를 대체할 gmtool의 user class
    """
    objects = GmManager()

    email = models.EmailField(verbose_name=_('email'), unique=True, max_length=100, )
    is_active = models.BooleanField(default=True, )
    is_superuser = models.BooleanField(default=False, )
    is_locked = models.BooleanField(default=False, )

    # AbstractBaseUser 내부에서 이미 존재하지만 상기할 겸 기입함.
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    #
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
    )

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        """
        user의 perm 보유 여부를 반환한다. superuser의 경우 모든 권한을 보유한 것으로 판단한다.
        :param perm: 확인할 권한.
        :param obj: ???
        :return: perm 보유 여부.
        """
        if self.is_superuser:
            return True
        # 우선 모두 True 반환.
        return True

    def has_module_perms(self, app_label):
        return True

    pass


#
# class GmExtends(models.Model):
#     """
#     gm user의 추가적인 속성들.[확장성 고려.]
#     """
#     from datetime import datetime, timedelta
#
#     @classmethod
#     def get_date_pw_valid(cls):
#         dt = cls.datetime.utcnow() + cls.timedelta(days=7)
#         return dt
#
#     gm = models.ForeignKey(
#         Gm,
#         related_name='extends',
#         related_query_name='extends',
#         on_delete=models.CASCADE,
#     )
#
#     date_pw_valid = models.DateTimeField(default=get_date_pw_valid)
#     date_registed = models.DateTimeField(default=datetime.utcnow)
#
#     pass
