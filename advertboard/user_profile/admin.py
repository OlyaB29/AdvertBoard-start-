from django.contrib import admin

from . models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Профиль пользователя
    list_display = ("user", "name", "phone")
    search_fields = ("user", "name", "phone")
    prepopulated_fields = {'slug': ('user', )}

