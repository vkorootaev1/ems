from django.db import models
from ems import settings


class AuthAudit(models.Model):

    "Модель журнала аутентификации"

    AUTH_CHOICES = (
        ('LOGIN', 'Вход'),
        ('LOGOUT', 'Выход'),
        ('FAILED', 'Неуспешная попытка входа')
    )

    type = models.CharField(
        max_length=6, choices=AUTH_CHOICES, verbose_name='Тип')
    username = models.CharField(
        max_length=150, blank=True, verbose_name='Имя пользователя')
    user_pk = models.BigIntegerField(
        blank=True, null=True, verbose_name='Первичный ключ пользователя')
    user_repr = models.TextField(
        blank=True, verbose_name='Отображение пользователя')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             blank=True, on_delete=models.SET_NULL, verbose_name='Пользователь')
    remote_ip = models.GenericIPAddressField(
        blank=True, null=True, verbose_name='IP-адрес')
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name='Время добавления')

    class Meta:
        verbose_name = 'Запись журнала аутентификации'
        verbose_name_plural = 'Запись журнала аутентификации'
        ordering = ['-timestamp', ]

    def __str__(self) -> str:
        return f'{self.id}, {self.get_type_display()}, {self.username}'
