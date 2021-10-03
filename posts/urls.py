from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^$', views.PostList.as_view(), name='all'),
    url(r'^new/', views.CreatePosts.as_view(), name='create'),
    url(r'^by/(?P<username>[-\w]+)',
        views.UserPost.as_view(), name='for_user'),
    url(r'by/<username>/<int:pk>/',
        views.PostDetail.as_view(), name='single'),
    url(r'^delete/(?P<pk>\d+)/$', views.DeletePost.as_view(), name='delete'),
]
