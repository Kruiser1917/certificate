from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_password(value):
    if len(value) < 8:
        raise ValidationError(_('Пароль должен содержать не менее 8 символов'))
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Пароль должен содержать хотя бы одну цифру'))

def validate_email_domain(value):
    allowed_domains = ['mail.ru', 'yandex.ru']
    domain = value.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(_(f'Допустимы только домены: {", ".join(allowed_domains)}'))

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.email:
            validate_email_domain(self.email)
        super().save(*args, **kwargs) 