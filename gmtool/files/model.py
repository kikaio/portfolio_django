import os
from django.db import models
from django.conf import settings

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


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

    img_orig = models.ImageField(null = True, blank = True, default='', upload_to='gmtool/images')
    img_thumb = ImageSpecField(
        source = 'img_orig', # 원본 image file 의 field 명
        processors = [ResizeToFill(100, 100)], #사이즈 설정.
        format = 'JPEG', # 저장 포멧
        options = {'quality':60} #저장 옵션
    )

    # img_thimb_2 = ProcessedImageField(
    #     upload_to='gmtool/thumbs',
    #     processors = [Thumbnail(100,100)],
    #     format = 'JPEG',
    #     options ={'quality':60},
    #     default=
    # )

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.path))
        super().delete(*args, **kwargs)
        pass

pass
