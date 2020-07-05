from gmtool.log.model import *
from gmtool.log.form import *

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.shortcuts import Http404
from django.urls import reverse_lazy


LOG_ROOT = 'gmtool/log'

class GmLogList(FormMixin,ListView):
	paginate_by = 10
	form_class = GmLogSearchForm
	form = None
	model = GmLog
	context_object_name = 'log_list'
	template_name = f'{LOG_ROOT}/gm_log_list.html'
	success_url = reverse_lazy('gmtool:gm-log-list')

	def get_queryset(self):
		if not self.form:
			self.form = self.get_form()
		self.queryset = self.form.get_search_query(self.model)
		return super().get_queryset()

	def post(self, request, *args, **kwargs):
		self.form = self.form_class(request.POST, *args, **kwargs)

		if not self.form.is_valid():
			return self.form_invalid(self.form)
		else :
			return self.form_valid(self.form)

	def form_valid(self, form):
		self.object_list = self.get_queryset()
		allow_empty = self.get_allow_empty()
		if not allow_empty:
			raise Http404(_(f"Empty list and '{self.__class__.__name__}s.allow_empty' is False."))

		context = self.get_context_data(
			object_list=self.object_list,
			form = form,
		)
		return self.render_to_response(context)

	def form_invalid(self, form):
		self.object_list = None
		context = self.get_context_data(
			object_list=[],
			form = form,
		)
		return self.render_to_response(context)
