from django.apps import AppConfig

""" Блок отвечающий за объявления для студентов от преподавателей или других сотрудников уч. заведения"""

class AdsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ads'
    verbose_name = 'Объявления'

    def ready(self):
        import ads.signals
