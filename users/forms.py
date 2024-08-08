from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.urls import reverse_lazy

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма для регистрации пользователя"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserRecoveryPasswordForm(StyleFormMixin, PasswordResetForm):
    """Форма для восстановления пароля пользователя"""
    class Meta:
        model = User
        fields = ('email',)
