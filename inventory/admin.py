from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType
from django import forms

from .models import *

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = [
        'is_superuser',
    ]
    def has_delete_permission(self, request, obj=None):
        is_superuser = request.user.is_superuser
        if is_superuser:
            return True
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
            }
        if not is_superuser:
            disabled_fields.add('user_permissions')

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)

class MyGroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')


    permissions = forms.ModelMultipleChoiceField(Permission.objects.exclude(
        content_type__app_label__in=[
            'auth',
            'admin',
            'sessions',
            'contenttypes'
        ]),
        widget=admin.widgets.FilteredSelectMultiple(('permissions'), False),)
    

    def __init__(self, *args, **kwargs):
        super(MyGroupAdminForm, self).__init__(*args, **kwargs)

class MyGroupAdmin(admin.ModelAdmin):
    form = MyGroupAdminForm
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Group, MyGroupAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Department)
admin.site.register(Unit)
admin.site.register(Item)
admin.site.register(Vendor)
admin.site.register(Subcategory)
admin.site.register(Warehouse)
admin.site.register(Vendor_Items)
class Demand_ItemsAdmin(admin.ModelAdmin):
    list_display = ('demand', 'item', 'stock')
admin.site.register(Demand_Items, Demand_ItemsAdmin)
admin.site.register(Order_Items)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Purchase)
admin.site.register(Purchase_Items)
admin.site.register(Employee)
class DemandAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_added', 'total_price', 'status')
admin.site.register(Demand, DemandAdmin)
admin.site.register(Tax)
admin.site.register(Manufacturer)
