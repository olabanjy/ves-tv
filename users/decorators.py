from django.shortcuts import redirect
from .models import UserProfile, UserSubscribtion


def allowed_users(function):
    def wrapper_func(request, *args, **kwargs):
        # fetch request body
        if "Msisdn" in request.headers:
            msisdn = request.headers["Msisdn"]
            if msisdn.startswith("0") and len(msisdn) == 11:
                msisdn = msisdn.replace("0", "234", 1)
            # check or create profile
            theUser, created = UserProfile.objects.get_or_create(phone=msisdn)
            fetchSubscribtion = UserSubscribtion.objects.filter(user=theUser)
            if fetchSubscribtion.exists():
                theSub = fetchSubscribtion.first()
                if theSub.sub_active == True:
                    return function(request, *args, **kwargs)
                else:
                    return redirect("core:onboarding")
            else:
                return redirect("core:onboarding")
        else:
            # redirect to subscribe page
            return redirect("core:onboarding")

    wrapper_func.__doc__ = function.__doc__
    wrapper_func.__name__ = function.__name__
    return wrapper_func


def allowed_admin(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("core:permission-denied")

        return wrapper_func

    return decorator
