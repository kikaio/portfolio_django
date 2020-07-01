
from django.urls import path
from gmtool import views

app_name='gmtool'

urlpatterns = [
    path('', views.index, name='index'),
    path('gm-login', views.gm_login, name='gm-login'),
    path('gm-logout', views.gm_logout, name='gm-logout'),
    path('gm-change-pw', views.gm_change_pw, name='gm-change-pw'),
    path('gm-register', views.gm_register, name='gm-register'),
    path('gm-reset-pw', views.gm_reset_pw, name='gm-reset-pw'),
    path('gm-reset-pw-req', views.gm_reset_pw_req, name='gm-reset-pw-req'),
    path('gm-reset-pw-token/<uidb64>/<token>', views.gm_reset_pw_token, name='gm-reset-pw-token'),
    path('gm-reset-pw-done', views.gm_reset_pw_done, name='gm-reset-pw-done'),
]