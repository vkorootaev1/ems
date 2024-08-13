from django.apps import AppConfig
from auditlog.apps import AuditlogConfig

""" Изменение настроек сторонних приложений Django """

class KnoxConfig(AppConfig):
    name = 'knox'
    verbose_name = 'Аутентификация'


class AuditLogConfig(AuditlogConfig):
    verbose_name = 'Логгирование'
