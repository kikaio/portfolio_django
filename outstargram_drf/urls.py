
from django.urls import path
from outstargram_drf import views

app_name = 'outstargrame_drf'

urlpatterns = [
    path('/', views.index, name='index')
]