from django.contrib import admin
from authaudit import models


@admin.register(models.AuthAudit)
class AuthAuditAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'type', 'username', 'user_pk',
                       'user_repr', 'user', 'remote_ip', 'timestamp', ]
    fields = ['id', 'type', 'username', 'user_pk',
              'user_repr', 'user', 'remote_ip', 'timestamp', ]
    list_display = ['id', 'type', 'user', ]
    search_fields = ['user__last_name', 'user__first_name', 'username', ]
    list_filter = ["type", ]
