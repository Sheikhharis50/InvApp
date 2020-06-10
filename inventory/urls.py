from django.urls import path
from . import views

urlpatterns = [

    #--> Category
    path('category/', views.category_list, name='category_list'),
    path('category/new/', views.category_new, name='category_new'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category/update/<int:id>/', views.category_update, name='category_update'),

    #--> Sub-Category
    path('subcategory/', views.subcategory_list, name='subcategory_list'),
    path('subcategory/new/', views.subcategory_new, name='subcategory_new'),
    path('subcategory/<int:id>/', views.subcategory_detail, name='subcategory_detail'),
    path('subcategory/delete/<int:id>/', views.subcategory_delete, name='subcategory_delete'),
    path('subcategory/update/<int:id>/', views.subcategory_update, name='subcategory_update'),

    #--> Warehouse
    path('warehouse/', views.warehouse_list, name='warehouse_list'),
    path('warehouse/new/', views.warehouse_new, name='warehouse_new'),
    path('warehouse/<int:id>/', views.warehouse_detail, name='warehouse_detail'),
    path('warehouse/delete/<int:id>/', views.warehouse_delete, name='warehouse_delete'),
    path('warehouse/update/<int:id>/', views.warehouse_update, name='warehouse_update'),
 
    #--> Item
    path('item/', views.item_list, name='item_list'),
    path('item/new/', views.item_new, name='item_new'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('item/item_partial_detail/<int:id>/', views.item_partial_detail, name='item_partial_detail'),
    path('item/delete/<int:id>/', views.item_delete, name='item_delete'),
    path('item/update/<int:id>/', views.item_update, name='item_update'),

    #--> Unit
    path('unit/', views.unit_list, name='unit_list'),
    path('unit/new/', views.unit_new, name='unit_new'),
    path('unit/<int:id>/', views.unit_detail, name='unit_detail'),
    path('unit/delete/<int:id>/', views.unit_delete, name='unit_delete'),
    path('unit/update/<int:id>/', views.unit_update, name='unit_update'),

    #--> Brand
    path('brand/', views.brand_list, name='brand_list'),
    path('brand/new/', views.brand_new, name='brand_new'),
    path('brand/<int:id>/', views.brand_detail, name='brand_detail'),
    path('brand/delete/<int:id>/', views.brand_delete, name='brand_delete'),
    path('brand/update/<int:id>/', views.brand_update, name='brand_update'),

    #--> Department
    path('department/', views.department_list, name='department_list'),
    path('department/new/', views.department_new, name='department_new'),
    path('department/<int:id>/', views.department_detail, name='department_detail'),
    path('department/delete/<int:id>/', views.department_delete, name='department_delete'),
    path('department/update/<int:id>/', views.department_update, name='department_update'),

    #--> Manufacturer
    path('manufacturer/', views.manufacturer_list, name='manufacturer_list'),
    path('manufacturer/new/', views.manufacturer_new, name='manufacturer_new'),
    path('manufacturer/<int:id>/', views.manufacturer_detail, name='manufacturer_detail'),
    path('manufacturer/delete/<int:id>/', views.manufacturer_delete, name='manufacturer_delete'),
    path('manufacturer/update/<int:id>/', views.manufacturer_update, name='manufacturer_update'),

    #--> Tax
    path('tax/', views.tax_list, name='tax_list'),
    path('tax/new/', views.tax_new, name='tax_new'),
    path('tax/<int:id>/', views.tax_detail, name='tax_detail'),
    path('tax/delete/<int:id>/', views.tax_delete, name='tax_delete'),
    path('tax/update/<int:id>/', views.tax_update, name='tax_update'),

    #--> Vendor
    path('vendor/', views.vendor_list, name='vendor_list'),
    path('vendor/new/', views.vendor_new, name='vendor_new'),
    path('vendor/<int:id>/', views.vendor_detail, name='vendor_detail'),
    path('vendor/delete/<int:id>/', views.vendor_delete, name='vendor_delete'),
    path('vendor/update/<int:id>/', views.vendor_update, name='vendor_update'),

    #--> Customer
    path('customer/', views.customer_list, name='customer_list'),
    path('customer/new/', views.customer_new, name='customer_new'),
    path('customer/<int:id>/', views.customer_detail, name='customer_detail'),
    path('customer/delete/<int:id>/', views.customer_delete, name='customer_delete'),
    path('customer/update/<int:id>/', views.customer_update, name='customer_update'),

    #--> Demand
    path('demand/', views.demand_list, name='demand_list'),
    path('demand/new/', views.demand_new, name='demand_new'),
    path('demand/<int:id>/', views.demand_detail, name='demand_detail'),
    path('demand/delete/<int:id>/', views.demand_delete, name='demand_delete'),
    path('demand/update/<int:id>/', views.demand_update, name='demand_update'),

]
