from . import views
from django.urls import path

urlpatterns = [
    path('temp/', views.temp, name="temp" ),

]