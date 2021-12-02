from django.views.generic import ListView, DetailView
from app_blogs.models import Blog, Post


class BlogListView(ListView):
    model = Blog
    context_object_name = 'blogs'
    # template_name = 'app_blogs/blog_list'


class BlogItemView(ListView):
    model = Post
    context_object_name = "posts"
    # template_name = "app_blogs/post_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(blog=self.kwargs["pk"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = Blog.objects.get(pk=self.kwargs["pk"])
        return context


class PostDetailView(DetailView):
    model = Post
