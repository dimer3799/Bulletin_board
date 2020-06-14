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
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.core.signing import BadSignature

from .models import AdvUser
from .forms import ChangeUserInfoForm, RegisterUserForm
from .utilities import signer


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
	# Выход из личного кабинета
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

class RegisterUserView(CreateView):
	# Регистрация пользователей
	maodel = AdvUser
	template_name = 'main/register_user.html'
	form_class = RegisterUserForm
	success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView):
	# Успешная регистрация
	template_name = 'main/register_done.html'


def user_activate(request, sign):
	# Активация пользователя
	try:
		username = signer.unsign(sign)
	except BadSignature:
		return render(request, 'main/bad_signature.html')
	user = get_object_or_404(AdvUser, username = username)
	if user.is_activated:
		template = 'main/user_is_activated.html'
	else:
		template = 'main/activation_done.html'
		user.is_active = True
		user.is_activated = True
		user.save()
	return render(request, template)