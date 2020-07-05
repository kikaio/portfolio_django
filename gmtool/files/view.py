from gmtool.files.form import *


from django.shortcuts import render, reverse, redirect
from django.views import generic



FILE_ROOT = 'gmtool/files'

def render_files(req, template_name:str='', context:dict={}):
    return render(req, f'{FILE_ROOT}/{template_name}', context)


def file_upload(req):
    context = {}
    if req.method == "POST":
        form = FileUploadForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            context['msg'] = _('file upload is complete')
    else:
        form = FileUploadForm()
        pass
    context['form'] = form
    return render_files(req, 'file_upload.html', context)


def image_upload(req):
    context = {}
    if req.method == 'POST':
        form = ImageUploadForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            context['msg'] = _("Upload is successed")
        else:
            context['msg'] = _("Upload is Failed, form data is invalid")
    else:
        form = ImageUploadForm()
    context['form'] = form
    return render_files(req, 'image_upload.html', context)
pass


class FileUploadedListView(generic.ListView):
    paginate_by = 10
    template_name = f'{FILE_ROOT}/file_list.html'
    context_object_name = 'file_list'
    model = FileUploadModel
    ordering = ['id', ]

    @classmethod
    def delete(cls, req, pk):
        if not req.user.is_superuser() and not req.user.has_perm('gmtool.delete_fileuploadmodel'):
            return redirect('gmtool:index')

        target = cls.model.objects.get(id=pk)
        target.delete()
        return redirect('gmtool:file-list')


class ImageUploadedListView(generic.ListView):
    paginate_by = 10
    template_name = f'{FILE_ROOT}/image_list.html'
    context_object_name = 'img_list'
    ordering = ['id', ]
    model = ImageUploadModel

    @classmethod
    def delete(cls, req, pk):
        if not req.user.is_superuser() and not req.user.has_perm('gmtool.delete_imageuploadmodel'):
            return redirect('gmtool:index')

        target = cls.model.objects.get(id=pk)
        target.delete()
        return redirect('gmtool:image-list')

