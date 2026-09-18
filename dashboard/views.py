from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import AdminUserCreateForm, AdminUserEditForm


MARKET_ITEMS = [
    {"symbol": "EUR/USD", "price": "1.0834", "change": "+0.18%", "direction": "up"},
    {"symbol": "GBP/USD", "price": "1.2710", "change": "+0.11%", "direction": "up"},
    {"symbol": "USD/JPY", "price": "148.22", "change": "-0.07%", "direction": "down"},
    {"symbol": "XAU/USD", "price": "2,416.80", "change": "+0.42%", "direction": "up"},
    {"symbol": "AAPL", "price": "226.31", "change": "+1.24%", "direction": "up"},
    {"symbol": "TSLA", "price": "243.87", "change": "-0.58%", "direction": "down"},
    {"symbol": "NVDA", "price": "121.36", "change": "+2.06%", "direction": "up"},
    {"symbol": "MSFT", "price": "419.09", "change": "+0.33%", "direction": "up"},
]


INVESTMENT_PACKAGES = [
    {"name": "Basic Package", "amount": "$500 - $4,999", "return": "Starter market exposure", "duration": "30 days"},
    {"name": "Medium Package", "amount": "$5,000 - $14,999", "return": "Balanced growth planning", "duration": "60 days"},
    {"name": "Premium Package", "amount": "$15,000+", "return": "Priority portfolio support", "duration": "90 days"},
]


def format_money(value):
    return f"${value:,.2f}"


def require_user_management(profile, permission):
    if profile.user.is_superuser or getattr(profile, permission):
        return
    raise PermissionDenied


@login_required
def home(request):
    profile = request.user.profile
    if profile.role in ["admin", "superuser"]:
        User = get_user_model()
        return render(
            request,
            "dashboard/admin_home.html",
            {
                "market_items": MARKET_ITEMS,
                "stats": {
                    "users": User.objects.count(),
                    "active_investments": 24,
                    "portfolio_value": "$184,920.00",
                    "pending_reviews": 3,
                },
            },
        )

    return render(
        request,
        "dashboard/home.html",
        {
            "market_items": MARKET_ITEMS,
            "summary": {
                "total_balance": format_money(profile.portfolio_balance),
                "invested_amount": "$20,500.00",
                "returns": "$4,250.60",
                "available": format_money(profile.portfolio_balance),
            },
            "investment_packages": INVESTMENT_PACKAGES,
            "bundles": [
                {"name": "Starter Bundle", "amount": "$5,000.00", "value": "$6,250.00", "duration": "30 Days", "progress": 67},
                {"name": "Growth Bundle", "amount": "$7,500.00", "value": "$11,175.00", "duration": "60 Days", "progress": 45},
                {"name": "Premium Bundle", "amount": "$8,000.00", "value": "$11,555.00", "duration": "90 Days", "progress": 23},
            ],
            "transactions": [
                {"title": "Wallet Deposit", "date": "20 Jun 2025", "amount": "+$3,000.00", "type": "credit"},
                {"title": "Growth Bundle Investment", "date": "19 Jun 2025", "amount": "-$5,000.00", "type": "debit"},
                {"title": "Referral Bonus", "date": "18 Jun 2025", "amount": "+$120.00", "type": "credit"},
            ],
        },
    )


@login_required
def users(request):
    profile = request.user.profile
    require_user_management(profile, "can_view_users")

    User = get_user_model()
    users_qs = User.objects.select_related("profile").order_by("username")
    return render(request, "dashboard/users.html", {"users": users_qs})


@login_required
def create_user(request):
    require_user_management(request.user.profile, "can_create_users")
    if request.method == "POST":
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect("dashboard:users")
    else:
        form = AdminUserCreateForm()
    return render(request, "dashboard/user_form.html", {"form": form, "title": "Create User", "button_label": "Create User"})


@login_required
def edit_user(request, user_id):
    require_user_management(request.user.profile, "can_edit_users")
    User = get_user_model()
    user_obj = get_object_or_404(User.objects.select_related("profile"), pk=user_id)
    if request.method == "POST":
        form = AdminUserEditForm(request.POST, request.FILES, instance=user_obj.profile, user=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect("dashboard:users")
    else:
        form = AdminUserEditForm(instance=user_obj.profile, user=user_obj)
    return render(
        request,
        "dashboard/user_form.html",
        {"form": form, "title": f"Edit {user_obj.username}", "button_label": "Save Changes", "user_obj": user_obj},
    )


@login_required
def delete_user(request, user_id):
    require_user_management(request.user.profile, "can_delete_users")
    User = get_user_model()
    user_obj = get_object_or_404(User, pk=user_id)
    if user_obj == request.user:
        messages.error(request, "You cannot delete your own account from here.")
        return redirect("dashboard:users")
    if request.method == "POST":
        user_obj.delete()
        messages.success(request, "User deleted successfully.")
        return redirect("dashboard:users")
    return render(request, "dashboard/user_confirm_delete.html", {"user_obj": user_obj})
