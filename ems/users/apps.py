from django.apps import AppConfig

""" Блок отвечающий за пользователей информационной системы """

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'
