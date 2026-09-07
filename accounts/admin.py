from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone_number", "can_view_users", "can_create_users", "can_edit_users", "can_delete_users")
    list_filter = ("role", "can_view_users", "can_create_users", "can_edit_users", "can_delete_users")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "phone_number")
