from . import views
from django.urls import path


urlpatterns = [
    path('dashboard', views.dashboard_view, name="dashboard_view" ),
]