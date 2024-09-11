from django.db import models
from django.db.models import CharField, ForeignKey
from django.core.validators import MaxValueValidator


#=============Обьявления
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    price = models.FloatField(blank=False)
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', related_name='post_set', blank=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title

#=============Отзывы
class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=False)
    stars = models.IntegerField(blank=False, validators=[MaxValueValidator(5)])
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.body

#=============Категории товаров
class Category(models.Model):
    name = CharField(max_length=100, blank=False, default='')
    owner = models.ForeignKey('auth.User', related_name='categories', on_delete=models.CASCADE)
    posts = models.ManyToManyField('Post', related_name='category_set', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name