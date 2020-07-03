
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

urlpatterns +=[
    path('perm-list', views.PermList.as_view(), name='perm-list'),
    path('perm/create', views.PermCreate.as_view(), name='perm-create'),
    path('perm/delete/<int:pk>', views.perm_delete, name='perm-delete'),

    path('gm-list', views.gm_list, name='gm-list'),
    path('gm_user/<int:pk>', views.GmUserDetailView.as_view(), name='gm-user-detail'),
    path('gm_user/<int:pk>/update/', views.GmUserUpdateView.as_view(), name='gm-user-update'),

    path('gm-perm-list', views.GmPermListView.as_view(), name='gm-perm-list'),
    path('gm-perm/<int:pk>/create', views.GmPermListView.as_view(), name='gm-perm-create'),
    path('gm-perm/<int:gm_pk>/<int:perm_pk>/delete', views.delete_gm_perm, name='gm-perm-delete'),
]