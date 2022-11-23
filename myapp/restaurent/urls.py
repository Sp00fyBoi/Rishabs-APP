from . import views
from django.urls import path

urlpatterns = [
    path('profile', views.profile_view_res, name="profile_view_res" ),
    path('dashboard', views.dashboard_view, name="dashboard_view" )

]