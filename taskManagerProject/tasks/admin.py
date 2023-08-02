from django.contrib import admin
from .models import Task

class CreateDate(admin.ModelAdmin):
    readonly_fields = ('createDate',)

# Register your models here.
admin.site.register(Task, CreateDate)