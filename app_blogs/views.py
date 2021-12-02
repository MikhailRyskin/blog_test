from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from app_blogs.models import Blog, Post, Subscription, Read


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

    def post(self, *args, **kwargs):
        Subscription.objects.create(
            user=self.request.user,
            blog=Blog.objects.get(pk=self.kwargs["pk"])
        )
        print('записали подписку в модель')
        return redirect('blog_list')


class PostDetailView(DetailView):
    model = Post

    def post(self, *args, **kwargs):
        Read.objects.create(
            user=self.request.user,
            post=Post.objects.get(pk=self.kwargs["pk"])
        )
        print('пометили пост как прочитанный')
        return redirect('blog_list')


class FeedListView(ListView):
    model = Post
    context_object_name = "feed_posts"
    template_name = "app_blogs/feed_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        in_subscriptions = Subscription.objects.filter(user=self.kwargs["pk"])
        blogs_in_sub = []
        for sub in in_subscriptions:
            blogs_in_sub.append(sub.blog_id)
        # print(blogs_in_sub)
        queryset = queryset.filter(blog_id__in=blogs_in_sub)
        return queryset
