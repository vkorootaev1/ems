from django.contrib import admin
from certificate import models


@admin.register(models.Certificate)
class CertificateAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'date_add', 'date_upd', ]
    fields = ['id', 'type', 'count', 'status',
              'user', 'user_give', 'date_add', 'date_upd', ]
    list_display = ['id', 'type', 'status', 'user', 'user_give', ]
    search_fields = ['id', 'user__last_name', 'user__first_name',
                     'type__name', 'user_give__last_name', 'user_give__first_name', ]
    autocomplete_fields = ['user', 'user_give', 'type',]


@admin.register(models.CertificateType)
class CertificateTypeAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['id', 'name', 'description',
              'is_active', ]
    list_display = ['id', 'name', ]
    search_fields = ['name', ]
