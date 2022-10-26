from django.urls import path
from .views import LoginView, IndexView, LogoutView, RegisterView, UserPreferencesView, ChangePasswordView

urlpatterns = [
    path('', IndexView, name = 'index-page'),
    path('login', LoginView, name = 'login-page'),
    path('register', RegisterView, name = 'register-page'),
    path('logout', LogoutView, name = 'logout-page'),
    path('user-preferences', UserPreferencesView, name = 'user-preferences'),
    path('change-password', ChangePasswordView, name = 'change-password')
]
