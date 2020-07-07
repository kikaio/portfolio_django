from django import forms
from gmtool.files.model import *


class FileUploadForm(forms.ModelForm):
	class Meta:
		model = FileUploadModel
		fields = ['title', 'file']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['file'].required = False


#pip install pillow
class ImageUploadForm(forms.ModelForm):
	class Meta:
		model = ImageUploadModel
		fields = ['file']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['file'].required = False