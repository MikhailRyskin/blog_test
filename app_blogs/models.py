from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from blog_test.settings import DEFAULT_FROM_EMAIL


class Blog(models.Model):
    """Модель блога"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, verbose_name='название блога')

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'

    def __str__(self):
        return self.name


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
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        subscribers_email = Subscription.objects.filter(blog=self.blog).values_list('user__email', flat=True)
        # нужно получить host
        ref = 'http://127.0.0.1:8000' + self.get_absolute_url()
        subject = 'added new post'
        message = f'В блоге "{self.blog.name}", на который вы подписаны, появился новый пост "{self.title}"\n {ref}'
        send_mail(subject, message, DEFAULT_FROM_EMAIL, subscribers_email, fail_silently=False)


class Subscription(models.Model):
    """Модель подписки пользователя на блог"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)


class Read(models.Model):
    """Модель поста, прочитанного пользователем)"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
