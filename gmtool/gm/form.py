from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.contrib.auth import login
from gmtool.gm.model import Gm
from django.utils.http import urlsafe_base64_decode

class GmCreateForm(forms.ModelForm):

    pw = forms.CharField(label='password', widget=forms.PasswordInput)
    pw_confirm = forms.CharField(label='password_confirm', widget=forms.PasswordInput)

    class Meta:
        model = Gm
        fields = ['email']

    def clean_pw_confirm(self):

        pw = self.clean_data.get('pw')
        pw_confirm = self.clean_data.get('pw_confirm')

        if pw != pw_confirm:
            raise forms.ValidationError(_("password don't match"))
        return pw_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['pw'])
        if commit:
            user.save()
        return user
    pass


class GmChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Gm
        fields = ['email', 'password', 'is_active', 'is_locked', ]

    def clean_pw(self):
        return self.initial['password']

    pass


class UserAdmin(BaseUserAdmin):
    form = GmChangeForm
    add_form = GmChangeForm

    list_display = ['email', 'last_login', 'is_admin']
    list_filter = ['is_admin']

    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('last_login',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    ]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    pass


class GmRegistForm(forms.ModelForm):

    pw_confirm = forms.CharField(widget=forms.PasswordInput, max_length=100, )
    password = forms.CharField(widget=forms.PasswordInput, max_length=100,)
    password.widget.attrs.update({
        "class": "form-control form-control-user",
        "placeholder": "Password"
    })

    pw_confirm.widget.attrs.update({
        "class": "form-control form-control-user",
        "placeholder": "Repeat Password"
    })

    class Meta:
        model = Gm
        fields = ['email', 'password', 'pw_confirm']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            "class" : "form-control form-control-user",
            "placeholder": "Email Address"
        })


    def clean_pw_confirm(self):
        pw = self.cleaned_data.get('password')
        pw_confirm = self.cleaned_data.get('pw_confirm')
        if pw != pw_confirm:
            raise forms.ValidationError(_("password doesn't match"))
        return pw_confirm

    def save(self, commit=True):
        email = self.cleaned_data['email']
        pw = self.cleaned_data['password']

        if Gm.objects.filter(email__exact=email).exists():
            raise forms.ValidationError(_('Already exist gm id'))
        Gm.objects.create_user(email, pw)
    pass


class GmLoginForm(forms.Form):

    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)

    email.widget.attrs.update({
        "class":"form-control form-control-user",
        "aria - describedby": "emailHelp",
        "placeholder":"Enter Email Address...",
    })
    password.widget.attrs.update({
        "class":"form-control form-control-user",
        "placeholder":"Password",
    })

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Gm.objects.filter(email__exact=email).exists():
            raise forms.ValidationError(_('This Gm is not exist'))
        return email

    def login(self,  request):
        from gmtool.log.model import GmLog

        email = self.cleaned_data['email']
        pw = self.cleaned_data['password']
        gm = authenticate(request, email=email, password=pw)
        if gm is None:
            return False
        else :
            login(request, gm)
            GmLog.save_log_login(request.user)
            return True


class GmChangePwForm(forms.ModelForm):
    from django.contrib.auth.hashers import check_password
    new_pw = forms.CharField(widget=forms.PasswordInput, max_length=100, )
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, )
    password.widget.attrs.update({
        "class": "form-control form-control-user",
        "placeholder": "Password",
    })
    new_pw.widget.attrs.update({
        "class": "form-control form-control-user",
        "placeholder": "new Password",
    })

    class Meta:
        model = Gm
        fields = ['password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        pass

    def clean_password(self):
        pw = self.cleaned_data['password']
        gm = self.request.user
        if self.check_password(pw, gm):
            raise forms.ValidationError(_('invalid password'))
        return pw

    def clean_new_pw(self):
        pw = self.cleaned_data['password']
        new_pw = self.cleaned_data['new_pw']
        if pw == new_pw:
            raise forms.ValidationError(_('new password must be different origin password'))
        return new_pw

    def save(self, commit=True):
        gm = self.request.user
        new_pw = self.cleaned_data['new_pw']
        gm.set_password(new_pw)
        gm.save()
        login(self.request, gm)
    pass


class GmPwResetForm(forms.Form):
    from django.core.mail import EmailMessage
    from django.conf import settings
    from django.template import loader

    email = forms.EmailField(max_length=100)
    email.widget.attrs.update({
        "class": "form-control form-control-user",
        "aria-describedby": "emailHelp",
        "placeholder": "Enter Email Address...",
    })
    template_name_req = 'gmtool:gm-reset-pw-req'


    def send_reset_mail(self, request):
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
        from django.contrib.auth.tokens import default_token_generator

        email = self.cleaned_data['email']
        if not Gm.objects.filter(email__exact=email).exists():
            raise Exception(_("this mail doesn't exists"))

        gm = Gm.objects.get(email__exact=email)
        c = {
            'email': email,
            'domain': request.META['HTTP_HOST'],
            'site_name': 'GmTool',
            'uid': urlsafe_base64_encode(force_bytes(gm.id)),
            'user': gm,
            'token': default_token_generator.make_token(gm),
            'protocol': 'http',
        }

        title = "Please Check, And gmtool account's Reset password"
        content = self.loader.render_to_string('gmtool/gm/reset_pw_template.txt', c)
        mail_to = self.cleaned_data['email']
        mail_from = 'gmtool@noreply.com'
        try:
            msg = self.EmailMessage(title, content, from_email= 'gmtool@noreply.com', to=[mail_to])
            msg.send()
        except Exception as e:
            raise Exception(_('send mail error'))
        pass




class GmPwTokenForm(forms.Form):
    from django.contrib.auth.tokens import PasswordResetTokenGenerator
    token_generator = PasswordResetTokenGenerator()

    template_name_done = 'gmtool:gm-reset-pw-done'

    pw = forms.CharField(widget=forms.PasswordInput)
    pw_confirm = forms.CharField(widget=forms.PasswordInput)

    pw.widget.attrs.update({
        "class": "form-control form-control-user",
        "placeholder": "Password",
    })

    pw_confirm.widget.attrs.update({
        "class": "form-control form-control-user",
        "placeholder": "Password confirm",
    })


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.token = kwargs.pop('token', None)
        uid = kwargs.pop('uid', None)
        if uid is not None:
            self.uid = urlsafe_base64_decode(uid).decode()
        else:
            self.uid = None
        super().__init__(*args, **kwargs)

    def clean_pw_confirm(self):
        pw = self.cleaned_data['pw']
        pw_confirm = self.cleaned_data['pw_confirm']
        if pw == pw_confirm:
            return pw_confirm

        raise forms.ValidationError(_('password, password confirm field is different'))

    def check_token(self):
        if self.uid is not None and  Gm.objects.filter(id__exact=self.uid).exists():
            gm = Gm.objects.get(id = self.uid)
            if self.token_generator.check_token(gm, self.token):
                self.request.user = gm
                if not authenticate(self.request):
                    pw = self.cleaned_data['pw']
                    gm.set_password(pw)
                    gm.save()
                    return True
        return False
