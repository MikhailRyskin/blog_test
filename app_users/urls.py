from django.urls import path
from app_users.views import AccountView, AnotherLoginView, AnotherLogoutView
from app_blogs.views import FeedListView

urlpatterns = [
    path('login', AnotherLoginView.as_view(), name='login'),
    path('logout', AnotherLogoutView.as_view(), name='logout'),
    path('<int:pk>', AccountView.as_view(), name='account'),
    path('feed/<int:pk>', FeedListView.as_view(), name='feed_list'),
]