
from django.urls import path
from gmtool import views

app_name='gmtool'

urlpatterns = [
    path('', views.index, name='index'),
]