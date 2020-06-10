from django.shortcuts import render, get_object_or_404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.http import Http404, HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

from .models import AdvUser
from .forms import ChangeUserInfoForm


# Create your views here.

def index(request):
	return render(request, 'main/index.html')

def other_page(request, page):
	try:
		template = get_template('main/' + page + '.html')
	except TemplateDoesNotExist:
		raise Http404
	return HttpResponse(template.render(request=request))

class BBLoginView(LoginView):
	template_name = 'main/login.html'

@login_required
def profile(request):
	return render(request, 'main/profile.html')

class BBLogoutView(LoginRequiredMixin, LogoutView):
	template_name = 'main/logout.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
	# Изменение личных данных пользователя
	model = AdvUser
	template_name = 'main/chenge_user_info.html'
	form_class = ChangeUserInfoForm
	success_url = reverse_lazy('main:profile')
	success_message = 'Личные данные пользователя изменены'

	def dispatch(self, request, *args, **keyargs):
		self.user_id = request.user.pk
		return super().dispatch(request, *args, **keyargs)

	def get_object(self, queryset = None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)

class BBPaswwordChangeViews(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
	# Изменение пароля пользователя
	template_name = 'main/password_change.html'
	success_url = reverse_lazy('main:profile')
	success_message = 'Пароль пользователя изменен'