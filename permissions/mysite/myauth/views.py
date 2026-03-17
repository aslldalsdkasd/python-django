from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .models import Profile

class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"

class MyLogoutView(LogoutView):
    http_method_names = ['post', 'get']
    next_page = reverse_lazy('myauth:login')

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, 'myauth/logout.html')

    def post(self, request, *args, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)

class CreateUserView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect('myauth:about-me')