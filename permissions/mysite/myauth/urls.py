from django.contrib.auth.views import LoginView
from django.urls import path


from .views import (
    AboutMeView,
    MyLogoutView,
    CreateUserView
)

app_name = "myauth"

urlpatterns = [
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path('logout/', MyLogoutView.as_view(),name="logout"),
    path("login/", LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True),
         name="login"),
    path('register/', CreateUserView.as_view(), name="register"),
]
