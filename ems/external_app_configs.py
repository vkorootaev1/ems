from django.apps import AppConfig
from auditlog.apps import AuditlogConfig


class KnoxConfig(AppConfig):
    name = 'knox'
    verbose_name = 'Аутентификация'


class AuditLogConfig(AuditlogConfig):
    verbose_name = 'Логгирование'
