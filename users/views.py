from random import choices
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserForm, UserRegisterForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user.verified:  # проверяем, подтвержден ли пользователь
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Your account is not verified.")
            return self.form_invalid(form)


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        digits = [str(i) for i in range(10)]
        verified_password = ''.join(choices(digits, k=8))
        user = form.save()
        user.verified = False
        user.verified_password = verified_password
        user.save()
        send_mail(
            subject='Поздравляем с регистрацией!',
            message=f'Подтвердите вашу регистрацию, нажмите на ссылку: http://127.0.0.1:8000/users/verifying?code={user.verified_password}\n ',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user