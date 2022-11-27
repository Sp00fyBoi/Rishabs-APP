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
        order = OrderModel.objects.get(pk=pk)
        
        if "del" in request.POST:
            order.is_delivered = True
            order.save()
        elif "pay" in request.POST:
            order.is_paid = True
            order.save()
        elif "can" in request.POST:
            order.delete()
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

        context = {
            'order':order
        }
        return render(request, 'restaurent/order_details.html',context)


    else:
        check = OrderModel.objects.filter(pk=pk)
        if len(check)>0:
            order = OrderModel.objects.get(pk=pk)
        else:
            return dashboard_view(request)
        
        str = ""
        
        for i in range(2,len(order.feedback)-2):
            str+=order.feedback[i]

        context = {
            'order':order,
            'feedback': str
        }
        return render(request, 'restaurent/order_details.html',context)