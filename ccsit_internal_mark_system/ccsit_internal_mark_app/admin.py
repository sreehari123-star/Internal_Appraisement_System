from django.contrib import admin
from .models import Notification


# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'created_at']
    search_fields = ['title', 'content']


admin.site.register(Notification, NotificationAdmin)