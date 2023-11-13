from django.db import models


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Контент')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    view_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'Новость: {self.title}'
    

class Comments(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
