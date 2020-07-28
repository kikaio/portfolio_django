
from django.urls import path
from outstargram_drf import views
from rest_framework.routers import DefaultRouter
from rest_framework.routers import format_suffix_patterns

app_name = 'outstargram-drf'

urlpatterns = [
    path('', views.index, name='index'),
    # path('gm-list', views.gm_list, name='gm-list'),
    # path('gm/<int:pk>', views.gm_detail, name='gm'),
    # path('author-list', views.author_list, name='author-list'),
    # path('author/<int:pk>', views.author_detail, name='author'),
    # path('gm-list', views.GmListAPI.as_view(), name='gm-list'),
    # path('gm/<int:pk>', views.GmDetailAPI.as_view(), name='gm'),
    # path('author-list', views.AuthorListAPI.as_view(), name='author-list'),
    # path('author/<int:pk>', views.AuthorDetailAPI.as_view(), name='author'),
    # path('gm-list', views.GmListMixin.as_view(), name='gm-list'),
    # path('gm/<int:pk>', views.GmDetailMixin.as_view(), name='gm'),
    # path('author-list', views.AuthorListMinxin.as_view(), name='author-list'),
    # path('author/<int:pk>', views.AuthorDetailMixin.as_view(), name='author'),
    path('gm-list', views.GmListGeneric.as_view(), name='gm-list'),
    path('gm/<int:pk>', views.GmDetailGeneric.as_view(), name='gm'),
    path('author-list', views.AuthorListGeneric.as_view(), name='author-list'),
    path('author/<int:pk>', views.AuthorDetailGeneric.as_view(), name='author'),

    path('post-list', views.PostListGeneric.as_view(), name='post-list'),
    path('post/<int:pk>', views.PostDetailGeneric.as_view(), name='post-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

