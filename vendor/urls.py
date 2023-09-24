from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "vendor"

urlpatterns = [
 path("after_login/", after_login, name="after_login"),
 path("dashboard/", vendor_dashboard, name="vendor-dashboard"),
 path("super-admin-dashboard/", super_admin_dashboard, name="super-admin-dashboard"),

 path("vendor/film/list", film_list, name="vendor-film-list"),
 path("vendor/film/add-new", login_required(CreateFilm.as_view()) , name="vendor-add-film"),
 path("vendor/show/list", show_list, name="vendor-show-list"),
 path("vendor/show/add-new", login_required(CreateShow.as_view()), name="vendor-add-show"),
]
