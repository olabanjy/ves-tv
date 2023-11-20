from django.contrib.auth.decorators import login_required


from django.shortcuts import redirect

# Create your views here.

from users import choices as user_choices


@login_required
def after_login(request):
    admin_profile = request.user.profile

    if admin_profile.role == user_choices.Roles.Vendor.value:
        return redirect("vendor:vendor-dashboard")
    elif (
        admin_profile.role == user_choices.Roles.SuperAdmin.value
        or admin_profile.role == user_choices.Roles.SystemAdmin.value
    ):
        return redirect("vendor:super-admin-dashboard")
