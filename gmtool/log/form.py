import json
from django import forms
from datetime import datetime, timedelta
from gmtool.log.enum import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


def get_def_when_from():
    return datetime.utcnow() + timedelta(days=-3)


def get_def_when_to():
    return datetime.utcnow()


def get_log_where_enums():
    return json.dump(LogCategoryEnum)


def get_log_cate_enums():
    return json.dump(LogGmAccountEnumWhat)

class GmLogSearchForm(forms.Form):
    choices_init = (
        (0, _('Entire')),
    )

    choices_where = (
        (LogCategoryEnum.NONE.value, _('Entire')),
        (LogCategoryEnum.GM_ACCOUNT.value, _('GM_ACCOUNT')),
        (LogCategoryEnum.GM_MANAGE.value, _('GM_MANAGE')),
    )

    choices_what_from_gmaccount = (
        (LogGmAccountEnumWhat.NONE.value, _('Entire')),
        (LogGmAccountEnumWhat.SIGN.value, _('SIGN')),
        (LogGmAccountEnumWhat.PASSWORD.value, _('PASSWORD')),
    )

    choices_what_from_gmmanage = (
        (LogGmManageEnumWhat.NONE.value, _('Entire')),
        (LogGmManageEnumWhat.PERMISSION.value, _('PERMISSION')),
    )

    choice_how_from_permission_gm_manage = (
        (LogGmAccountEnumHowPermission.NONE.value, _('Entire')),
        (LogGmAccountEnumHowPermission.EDIT.value, _('EIDT')),
    )

    choices_how_from_sign_gmaccount = (
        (LogGmAccountEnumHowSignGmAccount.NONE.value, _('Entire')),
        (LogGmAccountEnumHowSignGmAccount.REGIST.value, _('REGIST')),
        (LogGmAccountEnumHowSignGmAccount.LOG_IN.value, _('LOG_IN')),
        (LogGmAccountEnumHowSignGmAccount.LOG_OUT.value, _('LOG_OUT')),
        (LogGmAccountEnumHowSignGmAccount.LOCKED.value, _('LOCKED')),
        (LogGmAccountEnumHowSignGmAccount.DORMANT.value, _('DORMANT')),
        (LogGmAccountEnumHowSignGmAccount.ACTIVATE.value, _('ACTIVATE')),
    )

    choices_how_from_pw_gmaccount = (
        (LogGmAccountEnumHowPwGmAccount.NONE.value, _('Entire')),
        (LogGmAccountEnumHowPwGmAccount.PW_CHANGE.value, _('PW_CHANGE')),
        (LogGmAccountEnumHowPwGmAccount.PW_RESET.value, _('PW_RESET')),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cur_where = None
        cur_what = None
        cur_how = None
        # todo : tuple 벗기고 세련되게 dictionary 사용하도록 수정할 것.
        for ele in args:
            cur_where = ele.get('where')
            cur_what = ele.get('what')
            cur_how = ele.get('how')

        if (cur_where is None) or (cur_what is None) or (cur_how is None):
            return

        cur_where = int(cur_where)
        cur_what = int(cur_what)
        cur_how = int(cur_how)

        where_field = self.fields['where'];
        where_field.choices = self.choices_where
        where_field.initial = cur_where

        what_field = self.fields['what'];
        how_field = self.fields['how'];

        if cur_where == 0:
            what_field.choices = self.choices_init
            what_field.initial = 0
            how_field.choices = self.choices_init
            how_field.initial = 0
        elif cur_where == 1:
            what_field.choices = self.choices_what_from_gmaccount
            what_field.initial = cur_what
            if cur_what == 0:
                how_field.choices = self.choices_init
                how_field.initial = 0
            elif cur_what == 1:
                how_field.choices = self.choices_how_from_sign_gmaccount
                how_field.initial = cur_how
            elif cur_what == 2:
                how_field.choices = self.choices_how_from_pw_gmaccount
                how_field.initial = cur_how
        elif cur_where == 2:
            what_field.choices = self.choices_what_from_gmmanage
            what_field.initial = cur_what
            how_field.choices = self.choices_init
            how_field.initial = cur_how
        self.is_valid()

    def get_search_query(self, model_cls):
        q = None
        if not self.is_valid():
            return q

        txt = self.cleaned_data['who']
        where = self.cleaned_data['where']
        what = self.cleaned_data['what']
        how = self.cleaned_data['how']
        when_from = self.cleaned_data['when_from']
        when_to = self.cleaned_data['when_to']
        if txt == '':
            q = model_cls.objects.all()
        else:
            """
            SELECT GmLog.* FROM GmLog inner join GmUser 
            on GmUser.id=GmLog.id
            WHERE GmUser.email Like '%gjdudd%'
            """
            users = User.objects.filter(email__contains=txt)
            q = model_cls.objects.filter(gm__in=[gm.id for gm in users])

        if where != 0:
            q = q.filter(where__exact=where)

        if what != 0:
            q = q.filter(what__exact=what)

        if how != 0:
            q = q.filter(how__exact=how)

        if when_from:
            q = q.filter(date_logged__gte=when_from)

        if when_to:
            q = q.filter(date_logged__lte=when_to)
        return q

    who = forms.CharField(
        initial='',
        max_length=100,
        required=False
    )

    where = forms.TypedChoiceField(
        coerce=int,
        choices=choices_where,
        initial=choices_where[0],
        widget=forms.Select(attrs={'onchange': "whereSelectedFunc(this.value);"})
    )

    what = forms.TypedChoiceField(
        coerce=int,
        choices=choices_init,
        initial=choices_init[0],
        widget=forms.Select(attrs={'onchange': "whatSelectedFunc(this.value);"})
    )

    how = forms.TypedChoiceField(
        coerce=int,
        choices=choices_init,
        initial=choices_init[0],
        widget=forms.Select(attrs={'onchange': "howSelectedFunc(this.value);"})
    )

    desc = forms.CharField(
        initial='',
        max_length=100,
        required=False
    )
    # todo : date time picker 적용할 것.
    when_from = forms.DateTimeField(
        required=False,
        initial=get_def_when_from,
        input_formats=["%Y-%m-%d %H:%M:%S"],
    )

    when_to = forms.DateTimeField(
        required=False,
        initial=get_def_when_to,
        input_formats=["%Y-%m-%d %H:%M:%S"],
    )

    def clean_where(self):
        cur_where = self.cleaned_data.get('where')
        if cur_where is None:
            raise forms.ValidationError(_('Where Val is invalid'), code='invalid')
        return cur_where

    def clean_what(self):
        cur_what = self.cleaned_data.get('what')
        if cur_what is None:
            raise forms.ValidationError(_('what Val is invalid'), code='invalid')
        return cur_what

    def clean_how(self):
        cur_how = self.cleaned_data.get('how')
        if cur_how is None:
            raise forms.ValidationError(_('how Val is invalid'), code='invalid')
        return cur_how

    #####################
    @staticmethod
    def get_strs_from_choice_tuple(tuples):
        items = ["{0}".format(ele[1]) for ele in tuples]
        return json.dumps(items)

    def get_default_choices_str(self):
        return GmLogSearchForm.get_strs_from_choice_tuple(self.choices_init)

    def get_where_tuple_list(self):
        return GmLogSearchForm.get_strs_from_choice_tuple(self.choices_where)

    ######################

    def get_gm_account_what(self):
        return GmLogSearchForm.get_strs_from_choice_tuple(self.choices_what_from_gmaccount)

    def get_gm_account_sign_how(self):
        return GmLogSearchForm.get_strs_from_choice_tuple(self.choices_how_from_sign_gmaccount)

    def get_gm_account_password_how(self):
        return GmLogSearchForm.get_strs_from_choice_tuple(self.choices_how_from_pw_gmaccount)

    def get_gm_manage_what(self):
        return GmLogSearchForm.get_strs_from_choice_tuple(self.choices_what_from_gmmanage)

    def get_gm_manage_permission_how(self):
        return GmLogSearchForm.get_strs_from_choice_tuple(self.choice_how_from_permission_gm_manage)
