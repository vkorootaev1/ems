from django.apps import AppConfig

""" Блок отвечающий за аутентификацию """

class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth'
