from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users import models


@admin.register(models.User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('id', )}),
        (None, {'fields': ('username', 'password')}),
        (('Персональная информация'), {
         'fields': ('first_name', 'last_name', 'patronymic', 'email', 'photo')}),
        (
            ('Разрешения'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (None, {'fields': ('last_login', 'date_joined', 'date_updated', )}),
    )
    readonly_fields = ['id', 'date_updated', 'last_login', 'date_joined', ]
    search_fields = ['last_name', 'first_name', ]
    list_filter = ['is_active', 'is_staff', 'is_superuser', ]
    list_display = ['id', 'last_name', 'first_name', 'patronymic', ]


@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', ]
    search_fields = ['user__last_name', 'user__first_name', ]
    autocomplete_fields = ['user', ]


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'user', 'study_group', ]
    list_display = ['id', 'user', 'study_group', ]
    search_fields = ['user__last_name',
                     'user__first_name', 'study_group__name']
    autocomplete_fields = ['study_group', 'user', ]
    list_filter = ['is_active', ]


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'user', 'rank', 'job_title',
              'cathedra', 'courses', 'is_active', ]
    list_display = ['id', 'user', ]
    search_fields = ['user__last_name',
                     'user__first_name', ]
    autocomplete_fields = ['courses', 'cathedra', ]
    list_filter = ['is_active', 'cathedra', ]


@admin.register(models.PersonRole)
class PersonRoleAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'name', 'description', ]
    list_display = ['id', 'name', ]
    search_fields = ['name', ]


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'user', 'roles', 'is_active', ]
    list_display = ['id', 'user', ]
    search_fields = ['user__last_name', 'user__first_name', ]
    autocomplete_fields = ['user', 'roles', ]
    list_filter = ['is_active', 'roles', ]


@admin.register(models.ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'type', ]
    list_display = ['id', 'type', ]
    search_fields = ['type', ]


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'contact_ref', 'type', 'user', ]
    list_display = ['id', 'user', 'type', 'contact_ref', ]
    search_fields = ['user__last_name', 'user__first_name', 'type__type', ]
    autocomplete_fields = ['user', 'type', ]
    list_filter = ['type', ]
