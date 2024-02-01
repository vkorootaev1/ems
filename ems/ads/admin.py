from django.contrib import admin
from ads import models


@admin.register(models.Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'date_add', 'date_upd', ]
    fields = ['id', 'body', 'groups', 'user', 'date_add', 'date_upd', ]
    list_display = ['id', 'truncate_body', 'user', ]
    search_fields = ['id', 'user__last_name', 'user__first_name', ]
    autocomplete_fields = ['user', ]


@admin.register(models.AdvertisementFile)
class AdvertisementFileAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'date_add', ]
    fields = ['id', 'advertisement', 'origin_name',
              'file', 'user', 'date_add', ]
    list_display = ['id', 'origin_name', 'user', ]
    search_fields = ['advertisement__id',
                     'user__last_name', 'user__first_name']
    autocomplete_fields = ['user', 'advertisement']
