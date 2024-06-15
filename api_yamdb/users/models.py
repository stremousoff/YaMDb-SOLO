from django.contrib.auth.models import AbstractUser
from django.db import models

LIST_ROLE = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'админ'),
)


class CustomUser(AbstractUser):
    """Модель кастомного пользователя."""

    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=10, choices=LIST_ROLE, default='user')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
