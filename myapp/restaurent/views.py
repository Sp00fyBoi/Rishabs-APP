from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rishabs.models import OrderModel
# Create your views here.

@login_required(login_url='login_view')
def profile_view_res(request):
    return render(request, 'restaurent/profile.html')

@login_required(login_url='login_view')
def dashboard_view(request):
    orders = OrderModel.objects.all()
    total_revenue = 0
    for order in orders:
        total_revenue += order.price

    context = {
        'orders':orders,
        'total_revenue':total_revenue,
        'total_orders':len(orders),
    }
    return render(request, 'restaurent/dashboard.html',context)

#@login_required(login_url='login_view')
def order_details(request,pk):
    if request.method == "POST":
        return render(request, 'restaurent/dashboard.html',context)


    else:
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order':order
        }
        print(order)
        return render(request, 'restaurent/order_details.html',context)