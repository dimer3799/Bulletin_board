from django.urls import path
from .views import index, other_page, BBLoginView, profile, BBLogoutView, ChangeUserInfoView, BBPaswwordChangeViews, user_activate, RegisterUserView, RegisterDoneView

app_name = 'main'
urlpatterns = [
	path('accounts/register/activate/<str:sign>/', user_activate, name = 'register_activate'),
	path('accounts/register/done/', RegisterDoneView.as_view(), name = 'register_done'),
	path('account/register/', RegisterUserView.as_view(), name = 'register'),
	path('accounts/login/', BBLoginView.as_view(), name = 'login'),	
	path('accounts/password/change/',BBPaswwordChangeViews.as_view(), name = 'password_change'),
	path('accounts/profile/change/', ChangeUserInfoView.as_view(), name = 'profile_change'),	
	path('accounts/profile/', profile, name = 'profile'),
	path('accounts/logout/', BBLogoutView.as_view(), name = 'logout'),
	path('<str:page>/', other_page, name='other'),
	path('',index, name='index'),

]