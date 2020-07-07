import os
from django.db import models
from django.conf import settings

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class FileUploadModel(models.Model):

    title = models.CharField(max_length = 100)
    file = models.FileField(null=True)

    def delete(self, *args, **kwargs):
        file_path =os.path.join(settings.MEDIA_ROOT, self.file.path)
        os.remove(file_path)
        super().delete(*args, **kwargs)
pass


#pip install pillow, pilkit, django-imagekit
class ImageUploadModel(models.Model):
    """
    pillow, pilkit, django-imagekit 이 필요.
    """

    file = models.ImageField(null = True, blank = True, default='', upload_to='gmtool/')
    thumbnail = ImageSpecField(
        source = 'file', # 원본 image file 의 field 명
        processors = [ResizeToFill(100, 100)], #사이즈 설정.
        format = 'JPEG', # 저장 포멧
        options = {'quality':60} #저장 옵션
    )

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.path))
        super().delete(*args, **kwargs)
        pass

pass
