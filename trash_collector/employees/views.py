from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from .models import Employee
from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
from datetime import date
import calendar

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    user = request.user
    todays_date = date.today()
    employee_from_db = Employee.objects.get(user=user)
    zipcode = Customer.objects.filter(zipcode=employee_from_db.zipcode)
    weekly_pickup_day = Customer.objects.filter(weekly_pickup_day=calendar.day_name[todays_date.weekday()])
    #testing to make sure kevin is getting my changes 

    return render(request, 'employees/index.html', {'employee': employee_from_db, 'customers': zipcode, 'customers': weekly_pickup_day})
    


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
        

