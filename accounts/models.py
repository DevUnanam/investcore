from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        SUPERUSER = "superuser", "Superuser"
        ADMIN = "admin", "Admin"
        USER = "user", "User"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    phone_number = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    portfolio_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    can_view_users = models.BooleanField(default=False)
    can_create_users = models.BooleanField(default=False)
    can_edit_users = models.BooleanField(default=False)
    can_delete_users = models.BooleanField(default=False)
    can_activate_users = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def has_account_management_access(self):
        return self.user.is_superuser or self.role == self.Role.ADMIN or any(
            [
                self.can_view_users,
                self.can_create_users,
                self.can_edit_users,
                self.can_delete_users,
                self.can_activate_users,
            ]
        )
