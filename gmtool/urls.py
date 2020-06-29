
from django.urls import path
from gmtool import views

app_name='gmtool'

urlpatterns = [
    path('', views.index, name='index'),
    path('gm-login', views.gm_login, name='gm-login'),
    path('gm-change-pw', views.gm_change_pw, name='gm-change-pw'),
    path('gm-register', views.gm_register, name='gm-register'),
    path('gm-reset-pw', views.gm_reset_pw, name='gm-reset-pw'),
]