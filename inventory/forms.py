from django import forms
from django.forms import ModelChoiceField
from datetime import datetime
from .choices import cities, states, countries
from .itembarcode import getBarcode, makeBarcodeIMG
from .widgets import DatePickerInput, getCurrentDate
from .models import *

class CategoryForm(forms.ModelForm):

    name = forms.CharField(label='Category Name',
                           widget=forms.TextInput(attrs={
                               "class": "input-field"
                           })
                           )
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                      "class": "input-field",
                                      "rows": 5,
                                      "style": "border: 1px solid #cccccc",
                                  }), required=False
                                  )

    class Meta:
        model = Category
        fields = ('name', 'description', 'is_available')

class CategoryModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)
    def getID(self, obj):
        return obj.id
    
class SubCategoryForm(forms.ModelForm):

    name = forms.CharField(label='SubCategory Name',
                           widget=forms.TextInput(attrs={
                               "class": "fields"
                           })
                           )
    category = CategoryModelChoiceField(queryset=Category.objects.all(),
                                        widget=forms.Select(attrs={
                                            "class": "input-field select2 categories",
                                            'style': 'margin: .4rem 0;width:100%;',
                                            'data-placeholder': 'Select a Category',
                                            'id': '',
                                        }))
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                      "class": "fields",
                                      "rows": 5
                                  }), required=False
                                  )

    class Meta:
        model = Subcategory
        fields = ('name', 'description', 'category', 'is_available')

class SubCategoryModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class UnitForm(forms.ModelForm):
    name = forms.CharField(label='Unit Name',
                           widget=forms.TextInput(attrs={
                               "class": "input-field"
                           })
                           )

    class Meta:
        model = Unit
        fields = '__all__'

class UnitModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class WarehouseForm(forms.ModelForm):
    name = forms.CharField(label='Warehouse Name',
                           widget=forms.TextInput(attrs={
                                 "class": 'input-field'
                           })
                           )
    address = forms.CharField(label='Address', required=False,
                                  widget=forms.TextInput(attrs={
                                      "class": "input-field",
                                  })
                                  )
    city = forms.ChoiceField(label='City', required=False, choices=cities,
                             widget=forms.Select(
                                  attrs={
                                'data-placeholder': 'Select a City',
                                 "class": "input-field select2 city",
                                 'style': 'margin: .4rem 0;width:100%;',
                             })
                             )
    state = forms.ChoiceField(label='State', required=False, choices=states,
                              widget=forms.Select( attrs={
                                  "class": "input-field select2 state",
                                  'style': 'margin: .4rem 0;width:100%;',
                                  'data-placeholder': 'Select a State',
                              })
                              )
    country = forms.ChoiceField(label='Country', required=False, initial='Pakistan',
                                choices=countries,
                                widget=forms.Select(
                                attrs={
                                    "class": "input-field select2",
                                    'style': 'margin: .4rem 0;width:100%;',
                                    'data-placeholder': 'Select a Country',
                                })
                                )
    date_added = forms.DateField(label="Date Added", required=False,
                                 widget=DatePickerInput(attrs={
                                     'class': 'input-field',
                                     'value': getCurrentDate(),
                                 })
                                 )

    class Meta:
        model = Warehouse
        fields = '__all__'

class WarehouseModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class BrandForm(forms.ModelForm):
    name = forms.CharField(label='Brand Name',
                           widget=forms.TextInput(attrs={
                               "class": "input-field"
                           })
                           )
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                      "class": "input-field",
                                      "rows": 5,
                                      "style": "border: 1px solid #cccccc",
                                  }), required=False
                                  )

    class Meta:
        model = Brand
        fields = '__all__'

class BrandModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class DepartmentForm(forms.ModelForm):
    name = forms.CharField(label='Department Name',
                           widget=forms.TextInput(attrs={
                               "class": "input-field"
                           })
                           )
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                      "class": "input-field",
                                      "rows": 5,
                                      "style": "border: 1px solid #cccccc",
                                  }), required=False
                                  )
    contact = forms.CharField(label='Contact No',
                              widget=forms.TextInput(attrs={
                                  "class": "input-field"
                              }), required=False
                              )

    class Meta:
        model = Department
        fields = '__all__'

class DepartmentModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class ManufacturerForm(forms.ModelForm):
    name = forms.CharField(label='Manufacturer Name',
                           widget=forms.TextInput(attrs={
                               "class": "input-field"
                           })
                           )
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                      "class": "input-field",
                                      "rows": 5,
                                      "style": "border: 1px solid #cccccc",
                                  }), required=False
                                  )
    contact = forms.CharField(label='Contact No',
                              widget=forms.TextInput(attrs={
                                  "class": "input-field"
                              }), required=False
                              )
    address = forms.CharField(label='Address', required=False,
                              widget=forms.TextInput(attrs={
                                    "class": "input-field",
                              })
                              )
    city = forms.ChoiceField(label='City', required=False, choices=cities,
                             widget=forms.Select( attrs={
                                 "class": "input-field select2 city",
                                 'data-placeholder': 'Select a City',
                                 'style': 'margin: .4rem 0;width:100%;',
                           })
                           )
    state = forms.ChoiceField(label='State', required=False, choices=states,
                              widget=forms.Select( attrs={
                                  "class": "input-field select2 state",
                                  'data-placeholder': 'Select a State',
                                  'style': 'margin: .4rem 0;width:100%;',
                            })
                            )
    country = forms.ChoiceField(label='Country', required=False, choices=countries, initial='Pakistan',
                              widget=forms.Select( attrs={
                                    "class": "input-field select2",
                                    'style': 'margin: .4rem 0;width:100%;',
                                    'data-placeholder': 'Select a Country',
                              })
                              )

    class Meta:
        model = Manufacturer
        fields = '__all__'

class ManufacturerModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class TaxForm(forms.ModelForm):
    name = forms.CharField(label='Tax Name',
                           widget=forms.TextInput(attrs={
                               "class": "input-field"
                           })
                           )
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                      "class": "input-field",
                                      "rows": 5,
                                      "style": "border: 1px solid #cccccc",
                                  }), required=False
                                  )
    percentage = forms.FloatField(label='Percentage', required=False,
                                  widget=forms.NumberInput(attrs={
                                      "class": "input-field",
                                  })
                                  )

    class Meta:
        model = Tax
        fields = '__all__'

class TaxModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s,   %f%%" % (obj.name, obj.percentage)

class ItemForm(forms.ModelForm):
    name = forms.CharField(label='Item Name',
                           widget=forms.TextInput(attrs={
                                 "class": "input-field"
                           })
                           )
    price = forms.FloatField(label='Price', required=False,
                           widget=forms.NumberInput(attrs={
                               "class": "input-field",
                                'style': "height:38px",
                           })
                           )
    stock = forms.IntegerField(label='Stock', initial=1, required=False,
                             widget=forms.NumberInput(attrs={
                                 "class": "input-field",
                                 'style': "height:38px",
                             })
                             )
    reorder = forms.IntegerField(label='Reorder Point', required=False,
                               widget=forms.NumberInput(attrs={
                                   "class": "input-field",
                                   'style': "height:38px",
                               })
                               )
    cost = forms.FloatField(label='Cost', required=False,
                             widget=forms.NumberInput(attrs={
                                 "class": "input-field",
                                 'style': "height:38px",
                             })
                             )
    unit = UnitModelChoiceField(queryset=Unit.objects.all(),
                                required=True,
                                # empty_label='Select a Unit',
                                widget=forms.Select(attrs={
                                    "class": "input-field select2 units",
                                    'style': 'margin: .4rem 0;width:100%;',
                                    'id': '',
                                    'data-placeholder': 'Select a Unit',
                                })
                            )
    expiry_date = forms.DateField(label="Expiry Date", required=True,
                                  widget=DatePickerInput(attrs={
                                      'class': 'input-field',
                                      'value': getCurrentDate(),
                                      'style': 'border: 1px solid #e5e5e5',
                                  }))
    image = forms.ImageField(label='Item Image', required=False,
                         widget=forms.FileInput(attrs={
                              'id': 'up_item_img',
                              'alt':"Item Image", 
                              
                         })
                         )
    barcode = forms.CharField(required=False,
        label='Barcode', 
        widget=forms.TextInput(attrs={
                               "class": "input-field",
                               "readonly": "readonly",
                               "type" : "hidden",
                               "name" : "barcode",
                               }))
    barcodeImage = forms.ImageField(label='Barcode Image', required=False,
                                    widget=forms.FileInput(attrs={
                                        "class": "input-field",
                                        "width": "100",
                                        "height": "100",
                                    })
                                    )
    status = forms.ChoiceField(
        choices=[('Available', 'Available'),
                 ('N/A', 'N/A')], 
        widget=forms.Select(attrs={
            "class": "input-field select2",
            'style': 'margin: .4rem 0;width:100%;',
        }), required=False)
    category = CategoryModelChoiceField(queryset=Category.objects.all(), required=False,
                                        # empty_label='Select a Category',
                                        widget=forms.Select(attrs={
                                            "class": "input-field select2 categories",
                                            'style': 'margin: .4rem 0;width:100%;',
                                            'data-placeholder': 'Select a Category',
                                            'id': '',
                                        }))
    subcategory = SubCategoryModelChoiceField(queryset=Subcategory.objects.all(),
                                              required=False,
                                            #   empty_label='Select a SubCategory',
                                              widget=forms.Select(attrs={
                                                  "class": "input-field select2 subcategories",
                                                  'style': 'margin: .4rem 0;width:100%;',
                                                  'data-placeholder': 'Select a SubCategory',
                                                  'id': '',
                                              }))
    brand = BrandModelChoiceField(queryset=Brand.objects.all(), required=False,
                                        # empty_label='Select a Brand',
                                        widget=forms.Select(attrs={
                                            "class": "input-field select2 brands",
                                            'style': 'margin: .4rem 0;width:100%;',
                                            'id': '',
                                            'data-placeholder': 'Select a Brand',
                                        }))
    department = DepartmentModelChoiceField(queryset=Department.objects.all(), required=False,
                                #   empty_label='Select a Department',
                                  widget=forms.Select(attrs={
                                      "class": "input-field select2 departments",
                                      'style': 'margin: .4rem 0;width:100%;',
                                      'id': '',
                                      'data-placeholder': 'Select a Department',
                                  }))
    manufacturer = ManufacturerModelChoiceField(queryset=Manufacturer.objects.all(), required=False,
                                                # empty_label='Select a Manufacturer',
                                            widget=forms.Select(attrs={
                                                "class": "input-field select2 manufacturers",
                                                'id': '',
                                                'style': 'margin: .4rem 0;width:100%;',
                                                'data-placeholder': 'Select a Manufacturer',
                                            }))
    tax = TaxModelChoiceField(queryset=Tax.objects.all(), required=False,
                            #   empty_label='Select a Tax',
                              widget=forms.Select(attrs={
                                  "class": "input-field select2 taxes",
                                  'style': 'margin: .4rem 0;width:100%;',
                                  'id': '',
                                  'data-placeholder': 'Select a Tax',
                              }))
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                      "class": "input-field",
                                      "rows": 5,
                                      "style":"height:auto;"
                                  }), required=False
                                  )
    warehouse = WarehouseModelChoiceField(queryset=Warehouse.objects.all(), required=False,
                                        #   empty_label='Select a Warehouse',
                                          widget=forms.Select(attrs={
                                              "class": "input-field select2 warehouses",
                                              'style': 'margin: .4rem 0;width:100%;',
                                              'data-placeholder': 'Select a Warehouse',
                                              'id': '',
                                          }))
    date_added = forms.DateField(label="Date Added", required=False,
                                 widget=DatePickerInput(attrs={
                                     'class': 'input-field',
                                     'value': getCurrentDate(),
                                 })
                                 )

    class Meta:
        model = Item
        fields = '__all__'
    def clean_barcode(self):
        name = self.cleaned_data['name']
        code = self.cleaned_data['barcode']

        if len(str(code)) == 0:
            code = makeBarcodeIMG(getBarcode(), name)
        
        return code
    def clean_barcodeImage(self):
        code = self.cleaned_data['barcode']
        name = self.cleaned_data['name']

        return "barcodes//"+name+"_"+code+".png"
    
class VendorForm(forms.ModelForm):

    name = forms.CharField(label='Vendor Name',
                           widget=forms.TextInput(attrs={
                               "class": "input-field"
                           })
                           )
    address = forms.CharField(label='Address', required=False,
                              widget=forms.TextInput(attrs={
                                  "class": "input-field",
                              })
                              )
    city = forms.ChoiceField(label='City', required=False, choices=cities,
                             widget=forms.Select( attrs={
                                 "class": "input-field select2 city",
                                 'style': 'margin: .4rem 0;width:100%;',
                                 'data-placeholder': 'Select a City',
                           })
                           )
    state = forms.ChoiceField(label='State', required=False, choices=states,
                              widget=forms.Select( attrs={
                                  "class": "input-field select2 state",
                                  'style': 'margin: .4rem 0;width:100%;',
                                  'data-placeholder': 'Select a State',
                            })
                            )
    country = forms.ChoiceField(label='Country', required=False,
                                choices=countries, initial='Pakistan',
                                widget=forms.Select( attrs={
                                    "class": "input-field select2",
                                    'style': 'margin: .4rem 0;width:100%;',
                                    'data-placeholder': 'Select a Country',
                              })
                              )
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                      "class": "input-field",
                                      "rows": 5,
                                      "style": "border: 1px solid #cccccc",
                                  }), required=False
                                  )
    contact = forms.CharField(label='Contact No',
                              widget=forms.TextInput(attrs={
                                  "class": "input-field"
                              }), required=False
                              )
    date_added = forms.DateField(label="Date Added", required=False,
                                 widget=DatePickerInput(attrs={
                                     'class': 'input-field',
                                     'value': getCurrentDate(),
                                 })
                                 )

    class Meta:
        model = Vendor
        fields = '__all__'

class VendorModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

    def getID(self, obj):
        return obj.id

class CustomerForm(forms.ModelForm):

    first_name = forms.CharField(label='First Name',
                           widget=forms.TextInput(attrs={
                               "class": "input-field"
                           })
                           )
    last_name = forms.CharField(label='Last Name',
                                 widget=forms.TextInput(attrs={
                                     "class": "input-field"
                                 })
                                 )
    username = forms.CharField(label='Username',
                                 widget=forms.TextInput(attrs={
                                     "class": "input-field"
                                 })
                                 )
    email = forms.CharField(label='Email',required=False,
                            widget=forms.EmailInput(attrs={
                                "class": "input-field"
                            })
                            )
    password = forms.CharField(label='Password', required=False,
                               widget=forms.PasswordInput(attrs={
                                     "class": "input-field password",
                               })
                               )
    c_password = forms.CharField(label='Confirm Password', required=False,
                               widget=forms.PasswordInput(attrs={
                                   "class": "input-field c_password",
                               })
                               )
    address = forms.CharField(label='Address', required=False,
                              widget=forms.TextInput(attrs={
                                  "class": "input-field",
                              })
                              )
    city = forms.ChoiceField(label='City', required=False, choices=cities,
                             widget=forms.Select(attrs={
                                 "class": "input-field select2 city",
                                 'style': 'margin: .4rem 0;width:100%;',
                                 'data-placeholder': 'Select a City',
                             })
                             )
    state = forms.ChoiceField(label='State', required=False, choices=states,
                              widget=forms.Select(attrs={
                                  "class": "input-field select2 state",
                                  'style': 'margin: .4rem 0;width:100%;',
                                  'data-placeholder': 'Select a State',
                              })
                              )
    country = forms.ChoiceField(label='Country', required=False,
                                choices=countries, initial='Pakistan',
                                widget=forms.Select(attrs={
                                    "class": "input-field select2",
                                    'style': 'margin: .4rem 0;width:100%;',
                                    'data-placeholder': 'Select a Country',
                                })
                                )
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                      "class": "input-field",
                                      "rows": 5,
                                      "style": "border: 1px solid #cccccc",
                                  }), required=False
                                  )
    contact = forms.CharField(label='Contact No',
                              widget=forms.TextInput(attrs={
                                  "class": "input-field"
                              }), required=False
                              )
    date_added = forms.DateField(label="Date Added", required=False,
                                 widget=DatePickerInput(attrs={
                                     'class': 'input-field',
                                     'value': getCurrentDate(),
                                 })
                                 )

    class Meta:
        model = Customer
        fields = '__all__'

class CustomerModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.user.first_name, obj.user.last_name)
    def getID(self, obj):
        return obj.id

class DemandForm(forms.ModelForm):

    customer = CustomerModelChoiceField(queryset=Customer.objects.all(),
                                        widget=forms.Select(attrs={
                                            "class": "input-field select2 customers",
                                            'style': 'margin: .4rem 0;width:100%;',
                                            'data-placeholder': 'Select a Customer',
                                        }))
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                      "class": "input-field",
                                      "rows": 5,
                                      "style": "border: 1px solid #cccccc",
                                  }), required=False
                                  )
    total_price = forms.FloatField(label='Total Price', required=False,
                             widget=forms.NumberInput(attrs={
                                 "class": "input-field",
                                 'style': "height:38px",
                             })
                             )

    status = forms.ChoiceField(
        choices=[('Pending', 'Pending'),
                 ('Invoiced', 'Invoiced')],
        widget=forms.Select(attrs={
            "class": "input-field select2",
            'style': 'margin: .4rem 0;width:100%;',
        }), required=False)

    class Meta:
        model = Demand
        fields = '__all__'

class DemandModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.customer, obj.date_added)

    def getID(self, obj):
        return obj.id
