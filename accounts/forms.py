from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ["username", "first_name", "last_name", "email", "phone_number", "photo"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["username"].initial = self.user.username
        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name
        self.fields["email"].initial = self.user.email
        self.fields["phone_number"].label = "Phone number"
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def clean_username(self):
        username = self.cleaned_data["username"]
        User = get_user_model()
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        User = get_user_model()
        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.username = self.cleaned_data["username"]
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save()
            profile.save()
        return profile


class AdminUserCreateForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.Role.choices)
    phone_number = forms.CharField(max_length=30, required=False)
    portfolio_balance = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, initial=0)
    can_view_users = forms.BooleanField(required=False)
    can_create_users = forms.BooleanField(required=False)
    can_edit_users = forms.BooleanField(required=False)
    can_delete_users = forms.BooleanField(required=False)
    can_activate_users = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = self.cleaned_data["role"]
        profile.phone_number = self.cleaned_data["phone_number"]
        profile.portfolio_balance = self.cleaned_data["portfolio_balance"]
        profile.can_view_users = self.cleaned_data["can_view_users"]
        profile.can_create_users = self.cleaned_data["can_create_users"]
        profile.can_edit_users = self.cleaned_data["can_edit_users"]
        profile.can_delete_users = self.cleaned_data["can_delete_users"]
        profile.can_activate_users = self.cleaned_data["can_activate_users"]
        user.is_staff = profile.role in [Profile.Role.ADMIN, Profile.Role.SUPERUSER]
        user.is_superuser = profile.role == Profile.Role.SUPERUSER
        if commit:
            user.save()
            profile.save()
        return user


class AdminUserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    is_active = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "role",
            "phone_number",
            "portfolio_balance",
            "photo",
            "can_view_users",
            "can_create_users",
            "can_edit_users",
            "can_delete_users",
            "can_activate_users",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["username"].initial = self.user.username
        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name
        self.fields["email"].initial = self.user.email
        self.fields["is_active"].initial = self.user.is_active
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def clean_username(self):
        username = self.cleaned_data["username"]
        User = get_user_model()
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        User = get_user_model()
        if email and User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.username = self.cleaned_data["username"]
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]
        self.user.is_active = self.cleaned_data["is_active"]
        self.user.is_staff = profile.role in [Profile.Role.ADMIN, Profile.Role.SUPERUSER]
        self.user.is_superuser = profile.role == Profile.Role.SUPERUSER
        if commit:
            self.user.save()
            profile.save()
        return profile
