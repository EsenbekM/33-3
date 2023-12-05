from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=150, verbose_name='Название категории')

    def __str__(self):
        return f'Категория: {self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(BaseModel):
    title = models.CharField(max_length=150, verbose_name='Название тега')

    def __str__(self):
        return f'Тег: {self.title}'
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class News(models.Model):
    category = models.ForeignKey("news.Category", on_delete=models.CASCADE, 
                                 related_name='news', null=True, blank=True)
    tag = models.ManyToManyField("news.Tag", related_name='news', blank=True)
    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Контент')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    view_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'Новость: {self.title}'
    
    def get_category_name(self):
        if self.category is not None:
            return self.category.title
        return None

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    

class Comments(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
