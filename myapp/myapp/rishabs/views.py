from django.shortcuts import render
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from annoying.functions import get_object_or_None

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .models import MenuItem, Category, OrderModel

from rest_framework.decorators import api_view
from .helpers import send_otp_to_phone

# Create your views here.
@login_required(login_url='login_view')
def index(request):
    return render(request, 'rishabs/shop.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if User.objects.get(phone_number=username).is_phone_verified:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'rishabs/login.html', {'message': 'Invalid Credentials'})

    return render(request, 'rishabs/login.html')



def register_view(request):

    if request.method == "POST":
        name = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["cpassword"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]

        if password == password2 and password!=None:

            user = User.objects.create_user(
                username = name,
                password = password,
                phone_number = phone_number,
                otp = send_otp_to_phone(phone_number),
                email = email
            )
            user.set_password = password
            user.save()

            return render(request, 'rishabs/verify.html')

        else:
            return render(request, 'rishabs/register.html', {'message': 'Passwords do not match'})


    return render(request, 'rishabs/register.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login_view"))

@api_view(['POST'])
def verify(request):
    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        otp1 = request.POST["otp1"]

        try:
            user_obj = User.objects.get(phone_number = phone_number)

        except Exception as e:
            return render(request, 'rishabs/verify.html', {'message': 'Phone Number does not Exists'})
    
        if user_obj.otp == otp1:
            user_obj.is_phone_verified = True
            user_obj.save()
            return render(request, 'rishabs/shop.html')

        return render(request, 'rishabs/verify.html', {'message': 'Phone Number does not Exists'})

    else:
        return render(request, 'rishabs/verify.html')

def order(request):
    if request.method == "POST":

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')
        #print(items)
        for item in items:
            #print(item)
            menu_item = get_object_or_None(MenuItem, id=int(item))
            #print(menu_item)
            #menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(price=price)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }

        template = render_to_string('rishabs/email_template.html',context)

        email = EmailMessage(
            'Thanks for purchasing at Rishabs!',
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email],
        )


        email.fail_silently=False
        email.send()


        return render(request, 'rishabs/order_confirmation.html', context)

    else:

        juice = MenuItem.objects.filter(category__name__contains='juice')
        hot_drinks = MenuItem.objects.filter(category__name__contains='hot_drinks')
        snacks = MenuItem.objects.filter(category__name__contains='snacks')

        # pass into context
        context = {
            'juice': juice,
            'hot_drinks': hot_drinks,
            'snacks': snacks,
        }

        # render the template
        return render(request, 'rishabs/order.html', context)


def profile_view(request):
    return render(request, 'rishabs/profile.html')