from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


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
                "total_balance": "$24,750.60",
                "invested_amount": "$20,500.00",
                "returns": "$4,250.60",
                "available": "$4,250.60",
            },
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
    if not profile.has_account_management_access:
        raise PermissionDenied

    User = get_user_model()
    users_qs = User.objects.select_related("profile").order_by("username")
    return render(request, "dashboard/users.html", {"users": users_qs})
