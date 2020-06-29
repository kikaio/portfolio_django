from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group

from gmtool.gm.model import Gm

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


admin.site.register(Gm, UserAdmin)
admin.site.unregister(Group)
