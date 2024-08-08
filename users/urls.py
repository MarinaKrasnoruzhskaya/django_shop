from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path


from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserRecoveryPasswordView, ProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('recovery-password/', UserRecoveryPasswordView.as_view(), name='recovery_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
