from django.urls import path, include
from outstargram import views


app_name ='outstargram'

urlpatterns =[
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
]