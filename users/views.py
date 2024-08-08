import random
import secrets
import string

from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from config import settings
from users.forms import UserRegisterForm, UserRecoveryPasswordForm
from users.models import User


class UserCreateView(CreateView):
    """Контроллер для регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")  # после регистрации перенаправляем на вход#

    def form_valid(self, form):
        user = form.save()
        user.is_active = False  # регистрируем пользователя неактивным
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет! Перейди по ссылке {url} для подтверждения почты',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """Функция для верификации email"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserRecoveryPasswordView(PasswordResetView):
    """Контроллер для восстановления пароля"""
    model = User
    form_class = UserRecoveryPasswordForm
    template_name = 'users/recovery_password_form.html'
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        if self.request.method == 'POST':
            user_email = self.request.POST['email']
            try:
                user = User.objects.get(email=user_email)
                new_password = ''.join([random.choice(string.digits + string.ascii_letters) for _ in range(0, 10)])
                user.set_password(new_password)
                user.save()
                send_mail(
                    subject='Восстановление пароля',
                    message=f'Привет! Новый пароль {new_password} для входа в систему',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            except User.DoesNotExist:
                form.add_error(None, User.DoesNotExist(f"Пользователь {user_email} не найден"))
                return self.render_to_response(self.get_context_data(form=form))

        return redirect(reverse('users:login'))

