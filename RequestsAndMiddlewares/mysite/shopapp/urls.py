from django.urls import path
from .views import index, file_upload

urlpatterns = [
    path('', index, name='index' ),
    path('upload/', file_upload, name='file_upload'),
]