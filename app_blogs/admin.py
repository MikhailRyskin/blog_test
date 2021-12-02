from django.contrib import admin
from app_blogs.models import Blog, Post


class BlogAdmin(admin.ModelAdmin):
    fields = ('user', 'name')
    list_display = ('id','user', 'name')


class PostAdmin(admin.ModelAdmin):
    fields = ('blog', 'title', 'content')
    list_display = ('id', 'blog', 'title')


admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
