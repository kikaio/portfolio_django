from django import forms
from gmtool.files.model import *


class FileUploadForm(forms.ModelForm):
	class Meta:
		model = FileUploadModel
		fields = ['title', 'file']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['file'].required = False

		self.fields['title'].widget.attrs.update({
			"class": "form-control-sm",
		})
		self.fields['file'].widget.attrs.update({

		})
		pass


#pip install pillow
class ImageUploadForm(forms.ModelForm):
	class Meta:
		model = ImageUploadModel
		fields = ['img_orig']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['img_orig'].required = False
