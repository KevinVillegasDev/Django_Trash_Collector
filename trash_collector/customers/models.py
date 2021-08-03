from django.db import models
from django.db.models.fields import DateField, IntegerField
from django.db.models.fields.related import ForeignKey
# Create your models here.

# TODO: Finish customer model by adding necessary properties to fulfill user stories


class Customer(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    weekly_pickup_day = models.CharField(max_length=50)
    one_time_pickup = models.DateField(null=True)
    balance = IntegerField(default=0)
    suspend_start = DateField(null=True)
    suspend_end = DateField(null=True)
    
    def __str__(self):
        return self.name
    
