from django.apps import AppConfig


class AuthauditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authaudit'
    verbose_name = 'Аудит аутентификации'

    def ready(self) -> None:
        import authaudit.signals
