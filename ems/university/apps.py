from django.apps import AppConfig

""" Блок отвечающий за объекты уч. заведения (факультеты, кафедры, аудитории и т.д.)"""

class UniversityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'university'
    verbose_name = 'Университет'
