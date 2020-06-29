from django.contrib import admin
from . import models


class ClassAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Class)
admin.site.register(models.Priority)
admin.site.register(models.ClassGroup)
