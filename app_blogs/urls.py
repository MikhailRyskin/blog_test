from django.urls import path
from app_blogs.views import BlogListView, BlogItemView, PostDetailView

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('<int:pk>', BlogItemView.as_view(), name='blog'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
]
