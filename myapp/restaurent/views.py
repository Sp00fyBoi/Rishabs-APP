from django.shortcuts import render
# Create your views here.


def dashboard_view(request):
    return render(request,'restaurent/dashboard.html')