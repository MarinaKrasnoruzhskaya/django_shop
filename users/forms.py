from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, UserChangeForm

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


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Форма для редактирования профиля пользователя"""
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
