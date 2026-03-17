from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from .views import MyLogoutView, set_cookie, get_cookie, set_session_cookie, get_session_cookie

app_name = 'myauth'
urlpatterns = [
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('login/',
         LoginView.as_view(template_name='myauth/login.html',
                           redirect_authenticated_user=True, ),
         name='login'),


    path('set_cookie/', set_cookie, name='set_cookie'),
    path('get_cookie/', get_cookie, name='get_cookie'),

    path('set_session', set_session_cookie, name='set_session'),
    path('get_session', get_session_cookie, name='get_session'),
]