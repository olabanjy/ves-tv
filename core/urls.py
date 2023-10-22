from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "core"

urlpatterns = [
    path("", Homepage.as_view(), name="home"),
    path("channels/", channels, name="channels"),
    path("headers/", getRequestInfo, name="getRequestInfo"),
    path("echo/", echoView, name="echo"),
    path("watch/<slug>/", content_detail, name="content_detail"),
    path("like_product/", like_product, name="like_product"),
    path("watch-show/<slug>/", show_detail, name="show_detail"),
    path("watch/<content_slug>/<episode_slug>/", episode_detail, name="episode_detail"),
    path("category/<category_slug>/", category, name="category"),
    path("vendor-home/<vendor_code>/", vendor_home, name="vendor_home"),
    path("inactive_account/", inactive_account, name="inactive_account"),
    path("awaiting_response/", awaiting_response, name="awaiting_response"),
    path("onboarding/", onboarding, name="onboarding"),
]
