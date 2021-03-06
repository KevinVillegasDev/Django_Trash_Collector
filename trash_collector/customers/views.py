# from trash_collector import customers
from django.db.models.fields.related import ForeignKey
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Customer
from django.urls import reverse
# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


def index(request):
    # The following line will get the logged-in in user (if there is one) within any view function
    user = request.user

    try:
        # This line inside the 'try' will return the customer record of the logged-in user if one exists
        logged_in_customer = Customer.objects.get(user=user)
    except:
        # TODO: Redirect the user to a 'create' function to finish the registration process if no customer record found
        return HttpResponseRedirect(reverse('customers:create'))

    # It will be necessary while creating a Customer/Employee to assign request.user as the user foreign key

    print(user)
    return render(request, 'customers/index.html')

def create(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        weekly_pickup_day = request.POST.get('weekly_pickup_day')
        # one_time_pickup = request.POST.get('one_time_pickup')
        balance = request.POST.get('balance')
        # suspend_start = request.POST.get('suspend_start')
        # suspend_end = request.POST.get('suspend_end')
        new_customer = Customer(name = name, address = address, zipcode = zipcode, weekly_pickup_day = weekly_pickup_day,
                                balance = balance, user = user)
        new_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/create.html')
    
def details(request):
    user = request.user
    user_from_db = Customer.objects.get(user=user)
    return render(request, 'customers/details.html', {'customer': user_from_db})

def pickupday(request):
    user = request.user
    context = {"user": user}
    if request.method == "POST":
        weekly_pickup_day = Customer.objects.get(user=user)
        weekly_pickup_day.weekly_pickup_day = request.POST.get('weekly_pickup_day')
        weekly_pickup_day.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
         return render(request, 'customers/pickupday.html', context)
     
def onetimepickup(request):
    user = request.user
    context = {"user": user}
    if request.method == "POST":
        one_time_pickup = Customer.objects.get(user=user)
        one_time_pickup.one_time_pickup = request.POST.get('one_time_pickup')
        one_time_pickup.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
         return render(request, 'customers/onetimepickup.html', context)
    

    
def suspend(request):
    user = request.user
    context = {"user": user}
    if request.method == "POST":
        print(request.POST.get('suspend_start'))
        customer_to_suspend = Customer.objects.get(user=user)
        customer_to_suspend.suspend_start = request.POST.get('suspend_start')
        customer_to_suspend.suspend_end = request.POST.get('suspend_end')
        customer_to_suspend.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
         return render(request, 'customers/suspend.html', context)




# def balance(request):
#     user = request.user
#     context = {"user": user}
#     transaction_cost = 25.00
#     if request.method == "POST":
#         balance = Customer.objects.get(user = user) + 25
#         balance.balance = request.POST.get('balance')
#         # balance = transaction_cost * 4
#         balance.save()
#         return HttpResponseRedirect(reverse('customers:index'))
#     else:        
#         return render(request, 'customers/balance.html', context)