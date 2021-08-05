import datetime
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from .models import Employee
from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
from datetime import date
from datetime import timedelta
from django.db.models import Q
import calendar

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    user = request.user
    try:
        # This line inside the 'try' will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=user)
    except:
        return HttpResponseRedirect(reverse('employees:create'))
    todays_date = date.today()

    employee_from_db = Employee.objects.get(user=user)
    zip_pickup = Customer.objects.filter(zipcode=employee_from_db.zipcode)
    weekly_pickup = Customer.objects.filter(weekly_pickup_day=calendar.day_name[todays_date.weekday()])
    one_time =  Customer.objects.filter(one_time_pickup=todays_date).filter(zipcode=employee_from_db.zipcode)
    suspend_start = Customer.objects.filter(~Q(suspend_start=todays_date))
    
    
    customerSortResults= zip_pickup  & (weekly_pickup | one_time) & suspend_start

    return render(request, 'employees/index.html', {'employee': employee_from_db, 'customers': customerSortResults })
    


def create(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get("name")
        zipcode = request.POST.get("zipcode")
        new_employee = Employee(name=name,zipcode = zipcode, user = user)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index')) 
    else: 
        return render(request, 'employees/create.html')
        

