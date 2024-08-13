from django.contrib import admin
from university import models


@admin.register(models.Classroom)
class ClassroomStudyAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'name', 'description', 'number', 'house',
              'floor', 'is_active', ]
    list_display = ['id', 'number', 'floor',
                    'house', ]
    search_fields = ['name', 'number',
                     'house', 'floor', ]
    list_filter = ['house', 'floor', ]


@admin.register(models.Faculty)
class FacultyAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'name', 'description', 'is_active', ]
    list_display = ['id', 'name', ]
    search_fields = ['name', ]


@admin.register(models.Cathedra)
class CathedraAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'name', 'description', 'faculty', 'is_active', ]
    list_display = ['id', 'name', 'faculty', ]
    search_fields = ['name', 'faculty__name', ]
    list_filter = ['faculty', ]
    autocomplete_fields = ['faculty', ]


@admin.register(models.Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'code', 'name', 'description',
              'level_of_higher_education', 'study_period_months', 'form_of_study', 'cathedra', 'is_active', ]
    list_display = ['id', 'name', 'level_of_higher_education',
                    'form_of_study', 'cathedra', ]
    search_fields = ['name', 'cathedra__name', 'cathedra__faculty__name', ]
    list_filter = ['level_of_higher_education', 'form_of_study', 'is_active']
    autocomplete_fields = ['cathedra', ]
