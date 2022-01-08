from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView
from app_blogs.models import Blog, Post, Subscription, Read


class MainView(TemplateView):
    template_name = 'app_blogs/main.html'


class BlogListView(ListView):
    model = Blog
    context_object_name = 'blogs'


class BlogItemView(ListView):
    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(blog=self.kwargs["pk"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_subscription'] = Subscription.objects.filter(user=self.request.user,
                                                                 blog_id=self.kwargs["pk"]).exists()
        context['blog'] = Blog.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self, *args, **kwargs):
        if Subscription.objects.filter(user=self.request.user, blog_id=self.kwargs["pk"]).exists():
            Subscription.objects.filter(user=self.request.user,
                                        blog=Blog.objects.get(pk=self.kwargs["pk"])).delete()
        else:
            Subscription.objects.create(
                user=self.request.user,
                blog=Blog.objects.get(pk=self.kwargs["pk"])
            )
        return redirect('blog_list')


class PostDetailView(DetailView):
    model = Post

    def post(self, *args, **kwargs):
        Read.objects.create(
            user=self.request.user,
            post=Post.objects.get(pk=self.kwargs["pk"])
        )
        return redirect('blog_list')


class FeedListView(ListView):
    model = Post
    context_object_name = "feed_posts"
    template_name = "app_blogs/feed_list.html"

    def get_queryset(self):
        # через values_list
        # blogs_in_sub = Subscription.objects.filter(user=self.kwargs["pk"]).values_list('blog', flat=True)
        # read_posts = Read.objects.filter(user=self.kwargs["pk"]).values_list('post', flat=True)
        # queryset = Post.objects.filter(blog_id__in=blogs_in_sub).exclude(id__in=read_posts).order_by('-created_at')

        # через Subquery
        # blogs_in_sub = Subscription.objects.filter(user=self.kwargs["pk"])
        # read_posts = Read.objects.filter(user=self.kwargs["pk"])
        # queryset = Post.objects.filter(blog_id__in=Subquery(blogs_in_sub.values_list('blog', flat=True)
        #                                                     )).exclude(
        #     id__in=Subquery(read_posts.values_list('post', flat=True)
        #                     )).order_by('-created_at')

        queryset = Post.objects.filter(blog__subscription__user_id=self.kwargs["pk"]
                                       ).exclude(read__user_id=self.kwargs["pk"]).order_by('-created_at')
        return queryset
