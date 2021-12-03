from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from app_blogs.models import Post, Blog


class AccountView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'app_users/account.html'
    model = Post
    fields = ['title', 'content']

    def test_func(self):
        return self.request.user.pk == int(self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.blog = Blog.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)
        context["blog"] = user.blog
        return context


class AnotherLoginView(LoginView):
    template_name = 'app_users/login.html'


class AnotherLogoutView(LogoutView):
    template_name = 'app_users/logout.html'
