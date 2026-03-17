from django.urls import path
from .views import ArticleViewList
app_name = 'blogapp'
urlpatterns = [
    path('list/', ArticleViewList.as_view(), name='list'),
]