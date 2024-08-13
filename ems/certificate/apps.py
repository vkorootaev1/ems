from django.apps import AppConfig

""" Блок отвечающий за справки, связанные с уч. заведением"""

class CertificateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'certificate'
    verbose_name = 'Справки'
