from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "vendor"


admin_urls = [
    path("super-admin-dashboard/", super_admin_dashboard, name="super-admin-dashboard"),
    path("user-list/", user_list, name="user-list"),
    path("vendor-list/", all_vendors, name="vendor-list"),
    path("user-subs/", user_subs, name="user-subs"),
    path("content-list/", all_contents, name="content-list"),
    path("approve-content/<id>/", approve_content, name="approve-content"),
    path("approve-vendor/<id>/", approve_vendor, name="approve-vendor"),
]

vendor_urls = [
    path("dashboard/", vendor_dashboard, name="vendor-dashboard"),
    path("pending-verification/", pending_verification, name="pending-verification"),
    path("vendor/film/list/", film_list, name="vendor-film-list"),
    path("vendor/channel/list/", channel_list, name="channel-list"),
    path("vendor/channel/update/<channel_id>", update_channel, name="update-channel"),
    path(
        "vendor/channel/add-new",
        login_required(CreateChannel.as_view()),
        name="vendor-add-channel",
    ),
    path(
        "vendor/film/add-new",
        login_required(CreateFilm.as_view()),
        name="vendor-add-film",
    ),
    path("vendor/show/list", show_list, name="vendor-show-list"),
    path(
        "vendor/show/add-new",
        login_required(CreateShow.as_view()),
        name="vendor-add-show",
    ),
    path("profile-settings/", profile_settings, name="profile_settings"),
    path("complete_onboarding/", complete_onboarding, name="complete_onboarding"),
    path("submit_contract/", submit_contract, name="submit_contract"),
]


urlpatterns = (
    admin_urls
    + vendor_urls
    + [
        path("after_login/", after_login, name="after_login"),
    ]
)
