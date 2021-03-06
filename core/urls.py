from django.urls import path, include 
from .views import * 
from django.contrib.auth.decorators import login_required

app_name = 'core' 

urlpatterns = [

    path('',login_required(Homepage.as_view()), name='home'),

    path('watch/<slug>/', content_detail , name='content_detail'),

    path('watch/<content_slug>/<episode_slug>/', episode_detail , name='episode_detail'),

    path('category/<category_slug>/', category , name='category'),

]