from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from gmtool.log.enum import *
from django.contrib.auth import get_user_model

User = get_user_model()

class GmLog(models.Model):
    log_how_default = {
        0: _('Entire'),
    }

    log_what_default = {
        0: (_('Entire'), log_how_default),
    }

    log_where_default = {
        0: (_('Entire'), log_what_default),
    }

    log_how_dic_gmaccount_pw = {
        LogGmAccountEnumHowPwGmAccount.NONE.value: _('NONE'),
        LogGmAccountEnumHowPwGmAccount.PW_CHANGE.value: _('PW_CHANGE'),
        LogGmAccountEnumHowPwGmAccount.PW_RESET.value: _('PW_RESET'),
    }

    log_how_dic_gmaccount_sign = {
        LogGmAccountEnumHowSignGmAccount.NONE.value: _('Entire'),
        LogGmAccountEnumHowSignGmAccount.REGIST.value: _('REGIST'),
        LogGmAccountEnumHowSignGmAccount.LOG_IN.value: _('LOG_IN'),
        LogGmAccountEnumHowSignGmAccount.LOG_OUT.value: _('LOG_OUT'),
        LogGmAccountEnumHowSignGmAccount.LOCKED.value: _('LOCKED'),
        LogGmAccountEnumHowSignGmAccount.DORMANT.value: _('DORMANT'),
        LogGmAccountEnumHowSignGmAccount.ACTIVATE.value: _('ACTIVATE'),
    }

    log_what_dic_gm_account = {
        LogGmAccountEnumWhat.NONE.value: log_what_default[LogGmAccountEnumWhat.NONE.value],
        LogGmAccountEnumWhat.SIGN.value: (_('SIGN'), log_how_dic_gmaccount_sign),
        LogGmAccountEnumWhat.PASSWORD.value: (_('PASSWORD'), log_how_dic_gmaccount_pw),
    }

    log_what_dic_gm_manage = {

    }

    log_where_dic = {
        LogCategoryEnum.NONE.value: log_where_default[LogCategoryEnum.NONE.value],
        LogCategoryEnum.GM_ACCOUNT.value: (_('GM_ACCOUNT'), log_what_dic_gm_account),
        # LogCategoryEnum.GM_MANAGE.value : (_(''), log_what_dic_gm_manage),
        LogCategoryEnum.GM_MANAGE.value: (_('GM_MANAGE'), log_what_default),
    }

    class Meta:
        ordering = ('-date_logged',)
        verbose_name = _('log_gm_user')
        verbose_name_plural = _('log_gm_user')

    gm = models.ForeignKey(User, on_delete=models.CASCADE)
    date_logged = models.DateTimeField(
        _('logged date'),
        default=datetime.utcnow)

    # 추후 enum식으로 작업 할 것.
    where = models.IntegerField(_('where')
                                , default=0)
    what = models.IntegerField(_('what')
                               , default=0)
    how = models.IntegerField(_('how')
                              , default=0)
    desc = models.CharField(_('desc')
                            , max_length=100, default='')

    @classmethod
    def save_log_login(cls, gm):
        log = cls()
        log.save_log(who=gm,
                     where=LogCategoryEnum.GM_ACCOUNT.value,
                     what=LogGmAccountEnumWhat.SIGN.value,
                     how=LogGmAccountEnumHowSignGmAccount.LOG_IN.value,
                     )

    @classmethod
    def save_log_deactivate(cls, gm):
        log = cls()
        log.save_log(who=gm,
                     where=LogCategoryEnum.GM_ACCOUNT.value,
                     what=LogGmAccountEnumWhat.SIGN.value,
                     how=LogGmAccountEnumHowSignGmAccount.DORMANT.value,
                     )

    @classmethod
    def save_log_logout(cls, gm):
        log = cls()
        log.save_log(who=gm,
                     where=LogCategoryEnum.GM_ACCOUNT.value,
                     what=LogGmAccountEnumWhat.SIGN.value,
                     how=LogGmAccountEnumHowSignGmAccount.LOG_OUT.value,
                     )

    def save_log(self, where=0, who=0, what=0, how=0, desc=''):
        self.gm = who
        self.where = where
        self.what = what
        self.how = how
        self.desc = desc
        self.save()

    pass

    def get_str_where(self):
        return GmLog.log_where_dic[self.where][0]

    def get_str_what(self):
        try:
            cur_what_dic = GmLog.log_where_dic[self.where][1]
            return cur_what_dic[self.what][0]
        except Exception as e:
            return _('NONE')

    def get_str_how(self):
        cur_what_dic = GmLog.log_where_dic[self.where][1]
        cur_how_dic = cur_what_dic[self.what][1]
        return cur_how_dic[self.how]

