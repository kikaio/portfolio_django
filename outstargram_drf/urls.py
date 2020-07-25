
from django.urls import path
from outstargram_drf import views
from rest_framework.routers import DefaultRouter


app_name = 'outstargrame_drf'



urlpatterns = [
    path('/', views.index, name='index'),
]