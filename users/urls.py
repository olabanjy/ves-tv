from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "users"

urlpatterns = [
    # path("after_signup/", after_signup, name="after_signup"),
    # path("after_login/", after_login, name="after_login"),
    # path("awaiting_response/", awaiting_response, name="awaiting_response"),
    # path("onboarding/", onboarding, name="onboarding"),
    # path("inactive_account/", inactive_account, name="inactive_account"),
    # path("data_sync_endpoint/", data_sync, name="data_sync_endpoint"),
    path("after_signup/", after_signup, name="after_signup"),

    path("awaiting_response/", awaiting_response, name="awaiting_response"),
    path("onboarding/", onboarding, name="onboarding"),
    path("subscribe/", subscribe, name="subscribe"),
    path("cancelSubscribtion/", cancelSubscribtion, name="cancelSubscribtion"),
    path("inactive_account/", inactive_account, name="inactive_account"),
    path("data_sync_endpoint/", data_sync, name="data_sync_endpoint"),
    path("campaign_notification/", campaign_notification, name="campaign_notification"),
]
