from django.urls import path
from django.shortcuts import redirect

from gateway import views

app_name = 'gateway'

urlpatterns = [
    path('', views.index, name=''),
]