from django.contrib import admin
from .models import AppAdminuser


# Register your models here.
@admin.register(AppAdminuser)
class AppAdminuserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
