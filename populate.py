import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth import get_user_model

from accounts.models import Profile


DEFAULT_PASSWORD = "NervexDemo123!"

ACCOUNTS = [
    ("victoria_super", "Victoria", "Johnson", "victoria.super@nervex.ai", Profile.Role.SUPERUSER),
    ("daniel_super", "Daniel", "Okafor", "daniel.super@nervex.ai", Profile.Role.SUPERUSER),
    ("amina_admin", "Amina", "Okafor", "amina.admin@nervex.ai", Profile.Role.ADMIN),
    ("tunde_admin", "Tunde", "Bello", "tunde.admin@nervex.ai", Profile.Role.ADMIN),
    ("chika_admin", "Chika", "Nwosu", "chika.admin@nervex.ai", Profile.Role.ADMIN),
    ("alex_user", "Alex", "Johnson", "alex.user@example.com", Profile.Role.USER),
    ("sam_user", "Sam", "Williams", "sam.user@example.com", Profile.Role.USER),
    ("priya_user", "Priya", "Sharma", "priya.user@example.com", Profile.Role.USER),
    ("grace_user", "Grace", "Adams", "grace.user@example.com", Profile.Role.USER),
    ("michael_user", "Michael", "Brown", "michael.user@example.com", Profile.Role.USER),
]


def upsert_user(username, first_name, last_name, email, role):
    User = get_user_model()
    is_superuser = role == Profile.Role.SUPERUSER
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "is_staff": is_superuser,
            "is_superuser": is_superuser,
        },
    )
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.is_staff = is_superuser
    user.is_superuser = is_superuser
    if created:
        user.set_password(DEFAULT_PASSWORD)
    user.save()

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.role = role
    if is_superuser:
        profile.can_view_users = True
        profile.can_create_users = True
        profile.can_edit_users = True
        profile.can_delete_users = True
        profile.can_activate_users = True
    profile.save()
    return user, created


def run():
    print("Creating Nervex AI starter accounts...")
    for account in ACCOUNTS:
        user, created = upsert_user(*account)
        action = "created" if created else "updated"
        print(f"- {action}: {user.username}")
    print(f"Default password for newly created accounts: {DEFAULT_PASSWORD}")


if __name__ == "__main__":
    run()
