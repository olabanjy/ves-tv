from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "core"

urlpatterns = [
    path("", Homepage.as_view(), name="home"),
    path("channels/", channels, name="channels"),
    path("channels/<channel_id>/", channel_detail, name="channel_details"),
    path("headers/", getRequestInfo, name="getRequestInfo"),
    path("echo/", echoView, name="echo"),
    path("watch/<slug>/", content_detail, name="content_detail"),
    path("like_product/", like_product, name="like_product"),
    path("watch-show/<slug>/", show_detail, name="show_detail"),
    path("watch/<content_slug>/<episode_slug>/", episode_detail, name="episode_detail"),
    path("category/<category_slug>/", category, name="category"),
    path("genre/<genre_slug>/", genre, name="genre"),
    path("vendor-home/<vendor_code>/", vendor_home, name="vendor_home"),
    path("inactive_account/", inactive_account, name="inactive_account"),
    path("awaiting_response/", awaiting_response, name="awaiting_response"),
    path("onboarding/", onboarding, name="onboarding"),
    path("campaign/", campaign_url, name="onboarding"),
    path("become-a-vendor/", vendor_landing_page, name="vendor_landing_page"),
]
