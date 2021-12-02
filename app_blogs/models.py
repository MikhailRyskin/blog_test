from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    """Модель блога"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, verbose_name='название блога')

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    """Модель поста в блоге"""
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, verbose_name='заголовок')
    content = models.TextField(default='', verbose_name='содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return f'{self.title}'


class Subscription(models.Model):
    """Модель подписки на блог"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)


# class Feed(models.Model):
#     """Модель ленты новостей (постов)"""
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
#     is_read = models.BooleanField(default=False)


class Read(models.Model):
    """Модель постов, прочитанных пользователем)"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
