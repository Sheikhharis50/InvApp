from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from InvApp.settings import TEMPFILES_FOLDER, TEMPIMGS_FOLDER
import os

#+++++++++++++Some necessary Functions++++++++++++++++

def upload_location(instance, filename):
    filebase, extension = os.path.splitext(filename)
    _now = datetime.now()
    dt = _now.strftime("%d-%m-%Y_%H-%M-%S")
    return 'items/%s_%s.%s' % (instance.name, dt, extension)

#++++++++++++++++++++++++++++++++++++++++++++++++++++

#==> category

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

#==> subcategory

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

#==> warehouse

class Warehouse(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateField(default=datetime.now, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

#==> unit

class Unit(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

#==> brand

class Brand(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

#==> department

class Department(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name

#==> manufacturer

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

#==> tax

class Tax(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    percentage = models.FloatField()

#==> item

class Item(models.Model):
    name = models.CharField(max_length=60)
    price = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    stock = models.IntegerField(blank=True, default=1)
    returnable = models.BooleanField(default=True)
    reorder = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    barcode = models.CharField(
        max_length=25, blank=True)
    barcodeImage = models.ImageField(
        upload_to='barcodes/', blank=True, max_length=200)
    status = models.CharField(max_length=50,
                              choices=[('Available', 'Available'),
                                       ('N/A', 'N/A')],
                              default='Available')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateField(default=datetime.now, blank=True)
    date_updated = models.DateField(auto_now=True, blank=True)
    expiry_date = models.DateField(
        null=False, default=datetime.now, blank=False)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True)
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, blank=True
    )
    tax = models.ForeignKey(
        Tax, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_available = models.BooleanField(default=True, blank=False)


    def __str__(self):
        return self.name

#==> vendor

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True, blank=False)
    description = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateField(
        default=datetime.now, blank=True)

    def __str__(self):
        return self.name

#==> vendor_items

class Vendor_Items(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.vendor.name + ' | ' + self.item.name

#==> customer

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organization = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateField(default=datetime.now, blank=True)
    is_available = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

#==> Employee

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    organization = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

#==> order

class Order(models.Model):
    date_ordered = models.DateField(
        default=datetime.now, blank=True)
    total_price = models.FloatField(help_text="eg: 5000")
    advance = models.FloatField(help_text="eg: 200", blank=True, null=True)
    adjustment = models.FloatField(
        help_text="eg: +200 or -200", blank=True, null=True)
    discount = models.FloatField(help_text="eg: 300", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, 
                              choices=[('Pending', 'Pending'),
                                       ('Paid', 'Paid')])
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.invoice

#==> order_items

class Order_Items(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField(default=1)
    bundles = models.FloatField(default=1)

    def __str__(self):
        return self.order

#==> order

class Purchase(models.Model):
    invoice = models.IntegerField()
    date_purchased = models.DateField(
        default=datetime.now, blank=True)
    total_price = models.FloatField(help_text="in Rupees eg: 5000")
    advance = models.FloatField(
        help_text="in Rupees eg: 200", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=[('Pending', 'Pending'),
                                       ('Paid', 'Paid')])
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, blank=True, null=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.invoice

#==> order_items

class Purchase_Items(models.Model):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField(default=1)
    bundles = models.FloatField(default=1)


    def __str__(self):
        return self.purchase

#==> Demand

class Demand(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_added = models.CharField(max_length=50,blank=True)
    total_price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10,choices=[('Pending', 'Pending'),
                                       ('Invoiced', 'Invoiced')])

    def __str__(self):
        return "%s %s" % (self.customer, self.date_added)

#==> Demand_items

class Demand_Items(models.Model):
    demand = models.ForeignKey(Demand, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    stock = models.FloatField(default=1)

    def __str__(self):
        return "%s %s" % (self.demand.customer, self.demand.date_added)
