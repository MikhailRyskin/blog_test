from django.urls import path
from app_users.views import AccountView, AnotherLoginView, AnotherLogoutView

urlpatterns = [
    path('login', AnotherLoginView.as_view(), name='login'),
    path('logout', AnotherLogoutView.as_view(), name='logout'),
    path('<int:pk>', AccountView.as_view(), name='account'),
]