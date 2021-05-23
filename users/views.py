from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django.contrib.auth import get_user_model
from .forms import LoginForm, UserCreateForm

User = get_user_model()

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'users/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'app/top.html'

class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    model = User
    form_class = UserCreateForm
    template_name = 'users/signup.html'
    success_url = '/users/login/'

    # def form_valid(self, form):
    #     messages.success(self.request, "完了しました")
    #     return redirect('/app')
 
    # def form_invalid(self, form):
    #     messages.warning(self.request, "完了できませんでした")
    #     return super().form_invalid(form)
