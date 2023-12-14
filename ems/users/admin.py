from django.contrib import admin
from users import models


admin.site.register(models.User)
admin.site.register(models.Contact)
admin.site.register(models.ContactType)
admin.site.register(models.Teacher)
