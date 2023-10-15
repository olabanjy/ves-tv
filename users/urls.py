from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "users"

urlpatterns = [

    path("after_signup/", after_signup, name="after_signup"),


    path("subscribe/", subscribe, name="subscribe"),
    path("cancelSubscribtion/", cancelSubscribtion, name="cancelSubscribtion"),

    path("data_sync_endpoint/", data_sync, name="data_sync_endpoint"),
    path("campaign_notification/", campaign_notification, name="campaign_notification"),
]
