from django.shortcuts import render
from rishabs.models import OrderModel
# Create your views here.


def dashboard_view(request):
    orders = OrderModel.objects.all()
    total_revenue = 0
    for order in orders:
        total_revenue += order.price

    context = {
        'orders':orders,
        'total_revenue':total_revenue,
        'total_orders':len(orders)
    }
    return render(request, 'rishabs/dashboard.html',context)