from django.contrib import admin
from .models import Template, Notification

# Register your models here.


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):

    list_display = ("name", "channel")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = ("template", "content", "name")
