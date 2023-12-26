import random
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserForm, UserRegisterForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'
    token = None

    def form_valid(self, form):
        new_user = form.save()

        if new_user.is_active is False:
            user_token = user_token_verification()
            form.instance.code_verification = user_token

            confirm_link = self.request.build_absolute_uri(
                reverse_lazy(
                    "users:register_confirm", kwargs={"token": user_token}
                )
            )

            self.token = user_token
        # Отправка письма
        send_mail(
            subject='Поздравляем с регистрацией',
            message=f'Вы зарегистрировались на нашей платформе!'
                    f'\n\nВаш код верификации: {user_token}'
                    f'\n\nИли перейдите по ссылке {confirm_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email])

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:verifying')


def user_token_verification():
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])


def register_confirm(request, token):
    user_info = token

    print(user_info)

    if user_id := user_info:
        print(user_id)
        user = get_object_or_404(User, code_verification=user_id)
        user.is_active = True
        user.save()
        return redirect(to=reverse_lazy("users:login"))
    else:
        return redirect(to=reverse_lazy("users:register"))


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user



