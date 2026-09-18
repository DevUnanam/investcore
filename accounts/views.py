from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm


@login_required
def profile(request):
    profile_obj = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile_obj, user=request.user)

    return render(request, "accounts/profile.html", {"form": form})


@login_required
def delete_profile_photo(request):
    if request.method == "POST":
        profile_obj = request.user.profile
        if profile_obj.photo:
            profile_obj.photo.delete(save=False)
            profile_obj.photo = None
            profile_obj.save(update_fields=["photo", "updated_at"])
            messages.success(request, "Profile image removed.")
    return redirect("accounts:profile")
