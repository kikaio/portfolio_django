from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, authenticate

from gmtool.log.model import *

User = get_user_model()

class PermCreateForm(forms.Form):

	content_types = forms.TypedChoiceField(
		coerce = int,
	)

	code = forms.CharField(max_length= 30)

	desc = forms.CharField(max_length = 50)

	def __init__(self, *args, **wkargs):
		super().__init__(*args, **wkargs)
		cur_content_field = self.fields['content_types']
		content_list = ContentType.objects.all()

		content_choices = ((content.id, content.model) for content in content_list)
		cur_content_field.choices = content_choices
		cur_content_field.initial = 0

	def clean_code(self):
		code = self.cleaned_data['code']
		if Permission.objects.filter(codename__exact=code).exists():
			raise forms.ValidationError(_('this code is duplicated'), code='invalid')
		return code

	def clean_content_types(self):
		ct = self.cleaned_data['content_types']
		if not ContentType.objects.filter(id__exact=ct).exists():
			raise forms.ValidationError(_('invalid content type'), code='invalid')
		return ct

	def save(self):
		new_perm = Permission.objects.create(
			content_type_id = int(self.cleaned_data['content_types']),
			codename = self.cleaned_data['code'],
			name = self.cleaned_data['desc'],
		)
		#redirect to success?
pass


class GmPermAddForm(forms.Form):

	gm_choice = forms.TypedChoiceField(
		coerce=int,
		initial=0,
	)
	perms_choice = forms.TypedChoiceField(
		coerce=int,
		initial=0,
	)

	cur_user = None

	def __init__(self, *args, **kwargs):
		import logging
		for ele in args:
			logging.error(f'{ele}')

		super().__init__(*args, **kwargs)
		gm_list = [ele for ele in User.objects.all()]
		perm_list = [ele for ele in Permission.objects.all()]

		none_choice_tuple = ((0, _('NONE')))
		gm_list_field = self.fields['gm_choice']
		perms_field = self.fields['perms_choice']

		self.cur_user = None
		self.cur_perm = None
		is_invalid = False

		if gm_list is None or len(gm_list) == 0:
			is_invalid = True
		if perm_list is None or len(perm_list) == 0:
			is_invalid = True

		if is_invalid:
			gm_list_field.choices = none_choice_tuple
			perms_field.choices = none_choice_tuple
		else:
			gm_list_field.choices = ((ele.id, ele.get_full_name()) for ele in gm_list)
			perms_field.choices = ((ele.id, ele.name) for ele in perm_list)

	def clean_gm_choice(self):
		user_id = self.cleaned_data['gm_choice']
		if User.objects.filter(id__exact=user_id).exists():
			self.cur_user = User.objects.get(id = user_id)
			return user_id
		raise forms.ValidationError(_('this user is not exist'))

	def clean_perms_choice(self):
		perm_id = self.cleaned_data['perms_choice']
		if not Permission.objects.filter(id__exact=perm_id).exists():
			raise forms.ValidationError(_('permission is not exsits '), code='invalid')
		self.cur_perm = Permission.objects.get(id = perm_id)

		if self.cur_user.has_perm(self.cur_perm):
			raise forms.ValidationError(_('already user have this permission '), code='invalid')
		return perm_id

	def add_perm_to_user(self):
		self.cur_user.user_permissions.add(self.cur_perm)
		pass
pass


class GmUserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'email', 'is_superuser', 'is_active', 'is_locked'
		]
	email = forms.CharField(disabled=True)
pass


class GmDeactivateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = [
			'email', 'password'
		]
	email = forms.CharField(
		disabled = True,
		label = _('Email'),
	)

	password = forms.CharField(
		widget = forms.PasswordInput,
		initial = '',
	)


	def clean_password(self):
		pw = self.cleaned_data.get('password')
		if pw is None:
			raise forms.ValidationError(_('password is required'))
		cur_gm_email = self.cleaned_data.get('email')
		if (cur_gm_email is None) or (cur_gm_email==''):
			raise forms.ValidationError(_('cur_user is not exist'))
		cur_user = authenticate(email=cur_gm_email, password=pw)
		if cur_user is None:
			raise forms.ValidationError(_('password is incollect'))
		return cur_user.password

	def save(self, commit = True):
		gm_user = self.instance
		gm_user.is_active = False
		return super().save(commit)

	def deactivate(self, req):
		gm = req.user
		GmLog.save_log_logout(gm)
		GmLog.save_log_deactivate(gm)
		logout(req)
pass