from django.urls import path

from .views import PostCreateApiView, AllPostListApiView, PostEditApiView, \
    PostDeleteApiView, PostListApiView

urlpatterns = [
    path('posts/add', PostCreateApiView.as_view(), name='post_add'),
    path('posts/all', AllPostListApiView.as_view(), name='post_list_all'),
    path('posts/edit/<str:slug>', PostEditApiView.as_view(), name='post_edit'),
    path('posts/delete/<str:slug>', PostDeleteApiView.as_view(), name='post_delete'),
    path('posts', PostListApiView.as_view(), name='post_list_published'),
]
