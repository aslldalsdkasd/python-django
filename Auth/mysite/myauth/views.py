from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


# Create your views here.


class MyLogoutView(LogoutView):
    http_method_names = ['post', 'get']
    next_page = reverse_lazy('myauth:login')

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, 'myauth/logout.html')

    def post(self, request, *args, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)


def set_cookie(request:HttpRequest) ->HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('username', 'admin', 3600)
    return response

def get_cookie(request:HttpRequest) -> HttpResponse:
    values = request.COOKIES.get('username', 'default')
    return HttpResponse(f'cookie -> {values}')


def get_session_cookie(request:HttpRequest) -> HttpResponse:
    value = request.session.get('username', 'default')
    return HttpResponse(f'cookie -> {value}')

def set_session_cookie(request:HttpRequest) -> HttpResponse:
    resp = request.session['username'] = 'admin'
    return HttpResponse(f'cookie -> {resp}')