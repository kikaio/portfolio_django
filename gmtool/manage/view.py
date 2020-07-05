
from gmtool.manage.model import *
from gmtool.manage.form import *

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.views import generic
from django.contrib.auth import get_user_model

User = get_user_model()

MANAGE_ROOT = 'gmtool/manage'

def render_manage(req, template_name, context:dict={}):
    return render(req, f'{MANAGE_ROOT}/{template_name}', context)


def gm_list(req):
    context={}
    choices = [
        'email',
    ]
    context['search_text'] = ''
    context['choice_field'] = 'email'
    context['choice_selected'] = 'email'
    context['choices'] = choices
    if req.method == 'GET':
        context['gm_user_list'] = User.objects.all()
    elif req.method == 'POST':
        context['search_text'] = req.POST['search_text']
        context['choice_field'] = req.POST['choice_field']
        context['choice_selected'] = req.POST['choice_field']
        gm_user_list = []
        if(context['search_text'] == ''):
            gm_user_list = User.objects.all()
        else:
            q = None
            if context['choice_field'] == 'email':
                gm_user_list = User.objects.filter(email__contains=context['search_text'])
            else:
                pass
        context['gm_user_list'] = gm_user_list
    return render_manage(req, 'gm_user_list.html', context)

class GmUserDetailView(generic.DetailView):
	model = User
	context_object_name = 'gm_user'
	template_name = f'{MANAGE_ROOT}/gm_user_detail.html'

	def get_object(self):
		data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return data
pass


class GmUserUpdateView(generic.UpdateView):
    model = User
    context_object_name = 'gm_user'
    template_name = f'{MANAGE_ROOT}/gm_user_update.html'

    success_url = reverse_lazy('blog:gm-user-list')
    form_class = GmUserUpdateForm


def gm_perm_list(req):
    return redirect(reverse('gmtool:index'))

def delete_gm_perm(req, gm_pk, perm_pk):
	gm = User.objects.get(id=gm_pk)
	if gm is not None:
		perm = Permission.objects.get(id=perm_pk)
		if perm is not None:
			gm.user_permissions.remove(perm)
	return redirect('gmtool:gm-perm-list')

def perm_delete(request, pk=0):
    Permission.objects.filter(id__exact=pk).delete()
    return redirect('gmtool:perm-list')

class PermList(generic.ListView):
    model = Permission
    context_object_name = 'perm_code_list'
    template_name =  f'{MANAGE_ROOT}/perm_list.html'
    ordering = ['content_type_id', 'id']
    pass


class PermCreate(generic.FormView):
    models = Permission
    form_class = PermCreateForm
    success_url = reverse_lazy('gmtool:perm-list')
    context_object_name = 'perm_code_list'
    template_name = f'{MANAGE_ROOT}/perm_create.html'

    def form_valid(sefl, form):
        form.save()
        return super().form_valid(form)
pass


class GmPermListView(generic.edit.FormMixin, generic.ListView):

    paginate_by = 10
    """docstring for GmPermListView"ListView"""
    template_name = f'{MANAGE_ROOT}/gm_perm_list.html'
    model = User
    context_object_name = "gm_user_list"
    ordering = ['id', ]

    gm_perm_dic = {}
    form_class = GmPermAddForm
    success_url = reverse_lazy('gmtool:gm-perm-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gm_perm_dic'] = self.gm_perm_dic
        return context

    def get_queryset(self):
        user_list = super().get_queryset()
        for user in user_list:
            if user.user_permissions is not None:
                self.gm_perm_dic[user.id] = [ele for ele in user.user_permissions.all()]
        return user_list

    def post(self, request, *args, **kwargs):
        self.form = self.form_class(request.POST)

        if self.form.is_valid():
            return self.form_valid(self.form)
        else:
            return self.form_invalid(self.form)

    def form_valid(self, form):
        form = self.form
        form.add_perm_to_user()
        return super().form_valid(form)

pass


class GmDeactivateView(generic.UpdateView):
    model = User
    context_object_name = 'gm_user'
    template_name = f'{MANAGE_ROOT}/gm_user_deactivate.html'

    paginate_by = 10

    success_url = reverse_lazy('gmtool:index')
    form_class = GmDeactivateForm

    def form_valid(self, form):
        "id, password 확인 후 실제 로그아웃, 로그처리 담당."
        form.deactivate(self.request)
        return super().form_valid(form)
