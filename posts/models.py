from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

def validate_age(user):
    if not user.birth_date:
        raise ValidationError('Дата рождения не указана')
    
    today = timezone.now().date()
    age = today.year - user.birth_date.year - ((today.month, today.day) < (user.birth_date.month, user.birth_date.day))
    
    if age < 18:
        raise ValidationError('Автор должен быть старше 18 лет')

def validate_title(value):
    forbidden_words = ['ерунда', 'глупость', 'чепуха']
    for word in forbidden_words:
        if word in value.lower():
            raise ValidationError(f'Заголовок содержит запрещенное слово: {word}')

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=100, validators=[validate_title])
    text = models.TextField('Текст')
    image = models.ImageField('Изображение', upload_to='posts/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name='posts', verbose_name='Автор')
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_created']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        validate_age(self.author)
        super().clean()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
                           related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                             related_name='comments', verbose_name='Автор')
    text = models.TextField('Текст')
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date_created']
    
    def __str__(self):
        return f'Комментарий от {self.author.username} к посту {self.post.title}' 