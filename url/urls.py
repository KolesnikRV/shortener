from django.urls import path, re_path

from .views import index, url_redirect

app_name = 'url'

urlpatterns = [
    path('', index, name='index'),
    re_path(r'^[a-z0-9!"#$%&()*+,.:;<=>]', url_redirect, name='redirect'),
]
