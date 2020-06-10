from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.contrib import messages, auth
from .forms import *
from .choices import states, cities
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .itembarcode import makeBarcodeIMG, getBarcode
from .widgets import getCurrentDate
from django.template import Context, loader
from django.template.loader import render_to_string

# @login_required
def index(request):
    if request.user.is_authenticated:
        return render(request, 'pages/index.html')
    messages.error(request, 'Error! Login First!')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ CATEGORY ++++++++++++++++++++++++++

def category_new(request):

    if request.user.is_authenticated:
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            name = request.POST['name'].lower()
            if Category.objects.filter(name__iexact=name).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Category Already Exists!'})
                messages.error(request, 'Error! Category Already Exists')
                return redirect('category_new')
            category = form.save(commit=False)
            category.save()
            
            if "modal" in request.POST:
                queryset = Category.objects.all().order_by('id').values('id', 'name')
                
                return JsonResponse({'results': list(queryset),
                                    'status':'categories',
                                    'selected':'Select a Category', 
                                    'message':'Category is added successfully!'})
            
            messages.success(request, 'Success! Category is saved')
            form = CategoryForm()
        
        context = {
            'form': form,
            'status': 'Add Category',
            'page_name': 'Form',
            'list': False,
        }
        
        return render(request, 'pages/category/category.html', context)
    return render(request, 'accounts/login.html')

def category_list(request):
    if request.user.is_authenticated:
        queryset = Category.objects.all().order_by('id')
        if 'query' in request.GET:
            query = request.GET['query']
            if query:
                if query.lower() == 'available':
                    or_lookup = (Q(is_available=True))
                elif query.lower() == 'n/a':
                    or_lookup = (Q(is_available=False))
                else:
                    or_lookup = (
                        Q(description__icontains=query) |
                        Q(name__icontains=query)
                    )
                queryset = queryset.filter(
                    or_lookup
                )
        # paginator = Paginator(queryset, 10)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        context = {
            'data': queryset,
            'status': 'Categories List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/category/category.html', context)
    
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def category_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Category, id=id)
        context = {
            'obj': obj,
            'status': 'Category Detail',
            'page_name': 'Detail',
            'list': False,
        }
        return render(request, 'pages/category/category.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def category_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Category, id=id)
        form = CategoryForm(request.POST or None, instance=obj)
        if form.is_valid() and request.method == 'POST':
            name = request.POST['name'].lower()
            if Category.objects.filter(name__iexact=name).exclude(id=id).exists():
                messages.error(request, 'Error! Category Already Exists')
                return HttpResponseRedirect('/inventory/category/update/%d/'%obj.id)
            form.save()
            messages.success(request, f'Success! Category "{obj.name}" is updated')
            return redirect('category_list')
        context = {
            'form': form,
            'status': 'Update Category',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/category/category.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def category_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Category, id=id)
        messages.success(request, f'Success! Category "{obj.name}" is Deleted')
        obj.delete()
        # queryset = Category.objects.all().order_by('id').values('id', 'name', 'is_available')
        # return JsonResponse({'message': f'Category "{obj.name}" is Deleted',
                            # 'results': list(queryset), 'status': 'category'})
        return redirect('category_list')
    
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ CATEGORY ++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ SUBCATEGORY ++++++++++++++++++++++++++

def subcategory_new(request):

    if request.user.is_authenticated:
        form = SubCategoryForm(request.POST or None)
        if form.is_valid():
            name = request.POST['name'].lower()
            if Subcategory.objects.filter(name__iexact=name).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Subcategory Already Exists!'})
                messages.error(request, 'Error! Subcategory Already Exists')
                return redirect('subcategory_new')
            
            subcategory = form.save(commit=False)
            subcategory.save()

            if "modal" in request.POST:
                queryset = Subcategory.objects.all().order_by('id').values(
                    'id', 'name'
                )

                return JsonResponse({'results': list(queryset),
                                     'status': 'subcategories',
                                     'selected': 'Select a Subcategory',
                                     'message': 'Subcategory is added successfully!'})
            
            messages.success(request, 'Success! Subcategory is saved')
            form = SubCategoryForm()

        context = {
            'form': form,
            'status': 'Add Subcategory',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/subcategory/subcategory.html', context)
    return render(request, 'accounts/login.html')

def subcategory_list(request):
    if request.user.is_authenticated:
        queryset = Subcategory.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Subcategories List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/subcategory/subcategory.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def subcategory_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Subcategory, id=id)
        context = {
            'obj': obj,
            'status': 'Subcategory Detail',
            'page_name': 'Detail',
            'list': False,
        }
        return render(request, 'pages/subcategory/subcategory.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def subcategory_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Subcategory, id=id)
        form = SubCategoryForm(request.POST or None, instance=obj)
        if form.is_valid() and request.method == 'POST':
            name = request.POST['name'].lower()
            if Subcategory.objects.filter(name__iexact=name).exclude(id=id).exists():
                messages.error(request, 'Error! Subcategory Already Exists')
                return HttpResponseRedirect('/inventory/subcategory/update/%d/' % obj.id)

            form.save()
            messages.success(request, f'Success! SubCategory "{obj.name}" is updated')
            return redirect('subcategory_list')
        context = {
            'form': form,
            'status': 'Update Subcategory',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/subcategory/subcategory.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def subcategory_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Subcategory, id=id)
        
        messages.success(request, f'Success! SubCategory "{obj.name}" is Deleted')
        obj.delete()
        return redirect('subcategory_list')

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ SUBCATEGORY ++++++++++++++++++++++++++

# +++++++++++++++++++++++++++++ WAREHOUSE ++++++++++++++++++++++++++++

def warehouse_new(request):
    if request.user.is_authenticated:
        form = WarehouseForm(request.POST or None)
        if form.is_valid() and request.method == 'POST':
            name = request.POST['name'].lower()
            if Warehouse.objects.filter(name__iexact=name).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Warehouse Already Exists!'})
                messages.error(request, 'Error! Warehouse Already Exists')
                return redirect('warehouse_new')

            warehouse = form.save(commit=False)
            warehouse.save()

            if "modal" in request.POST:
                queryset = Warehouse.objects.all().order_by('id').values('id', 'name')

                return JsonResponse({'results': list(queryset),
                                     'status': 'warehouses',
                                     'selected': 'Select a Warehouse',
                                     'message': 'Warehouse is added successfully!'})

            messages.success(request, 'Success! is saved')
            form = WarehouseForm()

        context = {
            'form': form,
            'status': 'Add Warehouse',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/warehouse/warehouse.html', context)
    return render(request, 'accounts/login.html')

def warehouse_list(request):
    if request.user.is_authenticated:
        queryset = Warehouse.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Warehouses List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/warehouse/warehouse.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def warehouse_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Warehouse, id=id)
        context = {
            'obj': obj,
            'status': 'Warehouse Detail',
            'page_name': 'Detail',
            'list': False,
        }
        return render(request, 'pages/warehouse/warehouse.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def warehouse_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Warehouse, id=id)
        form = WarehouseForm(request.POST or None, instance=obj)
        if form.is_valid():
            name = request.POST['name'].lower()
            if Warehouse.objects.filter(name__iexact=name).exclude(id=id).exists():
                messages.error(request, 'Error! Warehouse Already Exists')
                return HttpResponseRedirect('/inventory/warehouse/update/%d/' % obj.id)
            form.save()
            messages.success(request, f'Success! Category "{obj.name}" is updated')
            return redirect('warehouse_list')
        context = {
            'form': form,
            'status': 'Update Warehouse',
            'page_name': 'Form',
            'list': False,
            'obj' : obj,
        }
        return render(request, 'pages/warehouse/warehouse.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def warehouse_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Warehouse, id=id)
        messages.success(request, f'Success! Warehouse {obj.name} is Deleted')
        obj.delete()
        
        return redirect('warehouse_list')
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++++ WAREHOUSE ++++++++++++++++++++++++++++

# +++++++++++++++++++++++++++++ ITEM ++++++++++++++++++++++++++++

def item_new(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                name = request.POST['name'].lower()
                if Item.objects.filter(name__iexact=name).exists():
                    if "modal" in request.POST:
                        return JsonResponse({'message': 'Item Already Exists!'})
                    messages.error(request, 'Error! Item Already Exists')
                    return redirect('item_new')
            
                item = form.save()
                item.save()

                if "modal" in request.POST:
                    queryset = Item.objects.all().order_by('id').values('id', 'name', 'price')

                    return JsonResponse({'results': list(queryset),
                                        'status': 'items',
                                        'selected': 'Select a Item',
                                        'message': 'Item is added successfully!'})
                
                messages.success(request, 'Success! Item is saved')
        form = ItemForm()
        context = {
            'form': form,
            'status': 'Add Item',
            'page_name': 'Form',
            'list': False,
            'categories': list(Category.objects.all().order_by('id')),
            'cities': cities,
            'states':states,
            'countries':countries,
        }
        return render(request, 'pages/item/item.html', context)
    return render(request, 'accounts/login.html')

def item_list(request):
    if request.user.is_authenticated:
        queryset = Item.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Items List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/item/item.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def item_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Item, id=id)
        context = {
            'obj': obj,
            'status_of_img': 0,
            'status_of_barcode': 0,
            'status': 'Item Detail',
            'page_name': 'Detail',
            'list': False,
        }
        if len(str(obj.image)) == 0:
            context['status_of_img'] = 1
        if len(str(obj.barcodeImage)) == 0:
            context['status_of_barcode'] = 1
        return render(request, 'pages/item/item.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def item_partial_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Item, id=id)
        context = {
            'obj': obj,
            'status_of_img': 0,
            'status_of_barcode': 0,
            'status': 'Item Detail',
            'page_name': 'Detail',
            'list': False,
        }
        if len(str(obj.image)) == 0:
            context['status_of_img'] = 1
        if len(str(obj.barcodeImage)) == 0:
            context['status_of_barcode'] = 1
        return render(request, 'pages/item/item_partial_detail.html', context)

    raise Http404()

def item_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Item, id=id)
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    name = request.POST['name'].lower()
                    if Item.objects.filter(name__iexact=name).exclude(id=id).exists():
                        messages.error(request, 'Error! Item Already Exists')
                        return HttpResponseRedirect('/inventory/item/update/%d/' % obj.id)

                    # update the changes
                    obj.name = name
                    obj.price = request.POST['price']
                    obj.cost = request.POST['cost']
                    if len(request.FILES) != 0:
                        obj.image = request.FILES['image']

                    obj.status = request.POST['status']
                    if request.POST['category']:
                        obj.category = Category.objects.get(id=request.POST['category'])
                    if request.POST['subcategory']:
                        obj.subcategory = Subcategory.objects.get(id=request.POST['subcategory'])
                    if request.POST['warehouse']:
                        obj.warehouse = Warehouse.objects.get(id=request.POST['warehouse'])
                    if request.POST['unit']:
                        obj.unit = Unit.objects.get(id=request.POST['unit'])
                    if request.POST['department']:
                        obj.department = Department.objects.get(id=request.POST['department'])
                    if request.POST['brand']:
                        obj.brand = Brand.objects.get(id=request.POST['brand'])
                    if request.POST['manufacturer']:
                        obj.manufacturer = Manufacturer.objects.get(id=request.POST['manufacturer'])
                    if request.POST['tax']:
                        obj.tax = Tax.objects.get(id=request.POST['tax'])

                    obj.expiry_date = request.POST['expiry_date']
                    obj.stock = request.POST['stock']
                    if "returnable" in request.POST:
                        obj.returnable = True
                    else:
                        obj.returnable = False
                    obj.reorder = request.POST['reorder']
                    obj.description = request.POST['description']

                    obj.save()
                    messages.success(request, f'Success! Item "{obj.name}" is updated')
                    return redirect('item_list')
                except:
                    messages.error(request, 'Error! Server is not responding')
            else:
                messages.error(request, 'Error! Form is not valid')
        else:
            form = ItemForm(instance=obj)
        context = {
            'obj': obj,
            'status_of_img': 0,
            'status_of_barcode': 0,
            'form': form,
            'date': getCurrentDate(),
            'status': 'Update Item',
            'page_name': 'Form',
            'list': False,
        }
        if len(str(obj.image)) == 0:
            context['status_of_img'] = 1
        if len(str(obj.barcodeImage)) == 0:
            context['status_of_barcode'] = 1

        return render(request, 'pages/item/item.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def item_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Item, id=id)
        messages.success(request, f'Success! Item {obj.name} is Deleted')
        obj.delete()
        return redirect('item_list')
    
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++++ ITEM ++++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ UNIT ++++++++++++++++++++++++++

def unit_new(request):

    if request.user.is_authenticated:
        form = UnitForm(request.POST or None)
        if form.is_valid():
            name = request.POST['name'].lower()
            if Unit.objects.filter(name__iexact=name).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Unit Already Exists!'})
                messages.error(request, 'Error! Unit Already Exists')
                return redirect('unit_new')

            unit = form.save(commit=False)
            unit.save()

            if "modal" in request.POST:
                queryset = Unit.objects.all().order_by('id').values(
                    'id', 'name'
                )

                return JsonResponse({'results': list(queryset),
                                     'status': 'units',
                                     'selected': 'Select a Unit',
                                     'message': 'Unit is added successfully!'})

            messages.success(request, 'Success! Unit is saved')
            form = UnitForm()

        context = {
            'form': form,
            'status': 'Add Unit',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/unit/unit.html', context)
    return render(request, 'accounts/login.html')

def unit_list(request):
    if request.user.is_authenticated:
        queryset = Unit.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Units List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/unit/unit.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def unit_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Unit, id=id)
        context = {
            'obj': obj,
            'status': 'Unit Detail',
            'page_name': 'Detail',
            'list': False,
        }
        return render(request, 'pages/unit/unit.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def unit_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Unit, id=id)
        form = UnitForm(request.POST or None, instance=obj)
        if form.is_valid() and request.method == 'POST':
            name = request.POST['name'].lower()
            if Unit.objects.filter(name__iexact=name).exclude(id=id).exists():
                messages.error(request, 'Error! Unit Already Exists')
                return HttpResponseRedirect('/inventory/unit/update/%d/' % obj.id)

            form.save()
            messages.success(
                request, f'Success! Unit "{obj.name}" is updated')
            return redirect('unit_list')
        context = {
            'form': form,
            'status': 'Update Unit',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/unit/unit.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def unit_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Unit, id=id)

        messages.success(request, f'Success! Unit "{obj.name}" is Deleted')
        obj.delete()
        return redirect('unit_list')

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ UNIT ++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ BRAND ++++++++++++++++++++++++++

def brand_new(request):

    if request.user.is_authenticated:
        form = BrandForm(request.POST or None)
        if form.is_valid():
            name = request.POST['name'].lower()
            if Brand.objects.filter(name__iexact=name).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Brand Already Exists!'})
                messages.error(request, 'Error! Brand Already Exists')
                return redirect('brand_new')

            brand = form.save(commit=False)
            brand.save()

            if "modal" in request.POST:
                queryset = Brand.objects.all().order_by('id').values(
                    'id', 'name'
                )

                return JsonResponse({'results': list(queryset),
                                     'status': 'brands',
                                     'selected': 'Select a Brand',
                                     'message': 'Brand is added successfully!'})

            messages.success(request, 'Success! Brand is saved')
            form = BrandForm()

        context = {
            'form': form,
            'status': 'Add Brand',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/brand/brand.html', context)
    return render(request, 'accounts/login.html')

def brand_list(request):
    if request.user.is_authenticated:
        queryset = Brand.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Brands List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/brand/brand.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def brand_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Brand, id=id)
        context = {
            'obj': obj,
            'status': 'Brand Detail',
            'page_name': 'Detail',
            'list': False,
        }
        return render(request, 'pages/brand/brand.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def brand_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Brand, id=id)
        form = BrandForm(request.POST or None, instance=obj)
        if form.is_valid() and request.method == 'POST':
            name = request.POST['name'].lower()
            if Brand.objects.filter(name__iexact=name).exclude(id=id).exists():
                messages.error(request, 'Error! Brand Already Exists')
                return HttpResponseRedirect('/inventory/brand/update/%d/' % obj.id)

            form.save()
            messages.success(
                request, f'Success! Brand "{obj.name}" is updated')
            return redirect('brand_list')
        context = {
            'form': form,
            'status': 'Update Brand',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/brand/brand.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def brand_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Brand, id=id)

        messages.success(request, f'Success! Brand "{obj.name}" is Deleted')
        obj.delete()
        return redirect('brand_list')

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ BRAND ++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ DEPARTMENT ++++++++++++++++++++++++++

def department_new(request):

    if request.user.is_authenticated:
        form = DepartmentForm(request.POST or None)
        if form.is_valid():
            name = request.POST['name'].lower()
            if Department.objects.filter(name__iexact=name).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Department Already Exists!'})
                messages.error(request, 'Error! Department Already Exists')
                return redirect('department_new')

            department = form.save(commit=False)
            department.save()

            if "modal" in request.POST:
                queryset = Department.objects.all().order_by('id').values(
                    'id', 'name'
                )

                return JsonResponse({'results': list(queryset),
                                     'status': 'departments',
                                     'selected': 'Select a Department',
                                     'message': 'Department is added successfully!'})

            messages.success(request, 'Success! Department is saved')
            form = DepartmentForm()

        context = {
            'form': form,
            'status': 'Add Department',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/department/department.html', context)
    return render(request, 'accounts/login.html')

def department_list(request):
    if request.user.is_authenticated:
        queryset = Department.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Departments List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/department/department.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def department_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Department, id=id)
        context = {
            'obj': obj,
            'status': 'Department Detail',
            'page_name': 'Detail',
            'list': False,
        }
        return render(request, 'pages/department/department.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def department_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Department, id=id)
        form = DepartmentForm(request.POST or None, instance=obj)
        if form.is_valid() and request.method == 'POST':
            name = request.POST['name'].lower()
            if Department.objects.filter(name__iexact=name).exclude(id=id).exists():
                messages.error(request, 'Error! Department Already Exists')
                return HttpResponseRedirect('/inventory/department/update/%d/' % obj.id)

            form.save()
            messages.success(
                request, f'Success! Department "{obj.name}" is updated')
            return redirect('department_list')
        context = {
            'form': form,
            'status': 'Update Department',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/department/department.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def department_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Department, id=id)

        messages.success(request, f'Success! Department "{obj.name}" is Deleted')
        obj.delete()
        return redirect('department_list')

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ DEPARTMENT ++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ MANUFACTURER ++++++++++++++++++++++++++

def manufacturer_new(request):

    if request.user.is_authenticated:
        form = ManufacturerForm(request.POST or None)
        if form.is_valid():
            name = request.POST['name'].lower()
            if Manufacturer.objects.filter(name__iexact=name).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Manufacturer Already Exists!'})
                messages.error(request, 'Error! Manufacturer Already Exists')
                return redirect('manufacturer_new')

            manufacturer = form.save(commit=False)
            manufacturer.save()

            if "modal" in request.POST:
                queryset = Manufacturer.objects.all().order_by('id').values(
                    'id', 'name'
                )

                return JsonResponse({'results': list(queryset),
                                     'status': 'manufacturers',
                                     'selected': 'Select a Manufacturer',
                                     'message': 'Manufacturer is added successfully!'})

            messages.success(request, 'Success! Manufacturer is saved')
            form = ManufacturerForm()

        context = {
            'form': form,
            'status': 'Add Manufacturer',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/manufacturer/manufacturer.html', context)
    return render(request, 'accounts/login.html')

def manufacturer_list(request):
    if request.user.is_authenticated:
        queryset = Manufacturer.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Manufacturers List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/manufacturer/manufacturer.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def manufacturer_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Manufacturer, id=id)
        context = {
            'obj': obj,
            'status': 'Manufacturer Detail',
            'page_name': 'Detail',
            'list': False,
        }
        return render(request, 'pages/manufacturer/manufacturer.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def manufacturer_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Manufacturer, id=id)
        form = ManufacturerForm(request.POST or None, instance=obj)
        if form.is_valid() and request.method == 'POST':
            name = request.POST['name'].lower()
            if Manufacturer.objects.filter(name__iexact=name).exclude(id=id).exists():
                messages.error(request, 'Error! Manufacturer Already Exists')
                return HttpResponseRedirect('/inventory/manufacturer/update/%d/' % obj.id)

            form.save()
            messages.success(
                request, f'Success! Manufacturer "{obj.name}" is updated')
            return redirect('manufacturer_list')
        context = {
            'form': form,
            'status': 'Update Manufacturer',
            'page_name': 'Form',
            'list': False,
            'obj': obj,
        }
        return render(request, 'pages/manufacturer/manufacturer.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def manufacturer_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Manufacturer, id=id)

        messages.success(
            request, f'Success! Manufacturer "{obj.name}" is Deleted')
        obj.delete()
        return redirect('manufacturer_list')

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ MANUFACTURER ++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ TAX ++++++++++++++++++++++++++

def tax_new(request):

    if request.user.is_authenticated:
        form = TaxForm(request.POST or None)
        if form.is_valid():
            name = request.POST['name'].lower()
            if Tax.objects.filter(name__iexact=name).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Tax Already Exists!'})
                messages.error(request, 'Error! Tax Already Exists')
                return redirect('tax_new')

            tax = form.save(commit=False)
            tax.save()

            if "modal" in request.POST:
                queryset = Tax.objects.all().order_by('id').values(
                    'id', 'name', 'percentage'
                )

                return JsonResponse({'results': list(queryset),
                                     'status': 'taxes',
                                     'selected': 'Select a Tax',
                                     'message': 'Tax is added successfully!'})

            messages.success(request, 'Success! Tax is saved')
            form = TaxForm()

        context = {
            'form': form,
            'status': 'Add Tax',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/tax/tax.html', context)
    return render(request, 'accounts/login.html')

def tax_list(request):
    if request.user.is_authenticated:
        queryset = Tax.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Taxes List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/tax/tax.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def tax_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Tax, id=id)
        context = {
            'obj': obj,
            'status': 'Tax Detail',
            'page_name': 'Detail',
            'list': False,
        }
        return render(request, 'pages/tax/tax.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def tax_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Tax, id=id)
        form = TaxForm(request.POST or None, instance=obj)
        if form.is_valid() and request.method == 'POST':
            name = request.POST['name'].lower()
            if Tax.objects.filter(name__iexact=name).exclude(id=id).exists():
                messages.error(request, 'Error! Tax Already Exists')
                return HttpResponseRedirect('/inventory/tax/update/%d/' % obj.id)

            form.save()
            messages.success(
                request, f'Success! Tax "{obj.name}" is updated')
            return redirect('tax_list')
        context = {
            'form': form,
            'status': 'Update Tax',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/tax/tax.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def tax_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Tax, id=id)

        messages.success(request, f'Success! Tax "{obj.name}" is Deleted')
        obj.delete()
        return redirect('tax_list')

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ TAX ++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ VENDOR ++++++++++++++++++++++++++

def vendor_new(request):

    if request.user.is_authenticated:
        form = VendorForm(request.POST or None)
        if form.is_valid():
            name = request.POST['name'].lower()
            if Vendor.objects.filter(name__iexact=name).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Vendor Already Exists!'})
                messages.error(request, 'Error! Vendor Already Exists')
                return redirect('vendor_new')

            vendor = form.save(commit=False)
            vendor.save()

            # Adding Vendor Items
            i=0
            while i<int(request.POST['items_count']):
                if 'item'+str(i) in request.POST:
                    vi = Vendor_Items()
                    vi.vendor = vendor
                    vi.item = get_object_or_404(Item, id=int(request.POST['item'+str(i)]))
                else:
                    i += 1
                    continue
                if 'is_available'+str(i) in request.POST:
                    vi.is_available = True
                else:
                    vi.is_available = False
                vi.save(force_insert=True)
                i += 1
            

            if "modal" in request.POST:
                queryset = Vendor.objects.all().order_by('id').values(
                    'id', 'name'
                )

                return JsonResponse({'results': list(queryset),
                                     'status': 'vendors',
                                     'selected': 'Select a Vendor',
                                     'message': 'Vendor is added successfully!'})

            messages.success(request, 'Success! Vendor is saved')
            form = VendorForm()

        context = {
            'form': form,
            'status': 'Add Vendor',
            'page_name': 'Form',
            'list': False,
            'items': list(Item.objects.all().order_by('id').values('id', 'name')),
        }
        return render(request, 'pages/vendor/vendor.html', context)
    return render(request, 'accounts/login.html')

def vendor_list(request):
    if request.user.is_authenticated:
        queryset = Vendor.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Vendors List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/vendor/vendor.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def vendor_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Vendor, id=id)
        
        context = {
            'obj': obj,
            'status': 'Vendor Detail',
            'page_name': 'Detail',
            'list': False,
            'vendor_items': list(Vendor_Items.objects.filter(vendor=obj)),
        }
        return render(request, 'pages/vendor/vendor.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def vendor_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Vendor, id=id)
        form = VendorForm(request.POST or None, instance=obj)
        vendor_items = Vendor_Items.objects.filter(vendor=obj)
        if form.is_valid() and request.method == 'POST':
            name = request.POST['name'].lower()
            if Vendor.objects.filter(name__iexact=name).exclude(id=id).exists():
                messages.error(request, 'Error! Vendor Already Exists')
                return HttpResponseRedirect('/inventory/vendor/update/%d/' % obj.id)

            print(request.POST)
            form.save()
            vendor_items.delete()

            # Adding Vendor Items
            i = 0
            while i < int(request.POST['items_count'])+1:
                if 'item'+str(i) in request.POST:
                    vi = Vendor_Items()
                    vi.vendor = obj
                    vi.item = get_object_or_404(
                        Item, id=int(request.POST['item'+str(i)]))
                else:
                    i += 1
                    continue
                if 'is_available'+str(i) in request.POST:
                    vi.is_available = True
                else:
                    vi.is_available = False
                vi.save(force_insert=True)
                i += 1


            messages.success(
                request, f'Success! Vendor "{obj.name}" is updated')
            return redirect('vendor_list')
        
        context = {
            'form': form,
            'status': 'Update Vendor',
            'page_name': 'Form',
            'list': False,
            'obj': obj,
            'vendor_items': list(vendor_items),
            'items': list(Item.objects.all().order_by('id').values('id', 'name')),
            'len': len(list(vendor_items))+1,
        }
        return render(request, 'pages/vendor/vendor.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def vendor_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Vendor, id=id)

        Vendor_Items.objects.filter(vendor=obj).delete()
        messages.success(request, f'Success! Vendor "{obj.name}" is Deleted')
        obj.delete()
        return redirect('vendor_list')

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ VENDOR ++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ CUSTOMER ++++++++++++++++++++++++++

def customer_new(request):

    if request.user.is_authenticated:
        form = CustomerForm(request.POST or None)
        if request.method == 'POST':

            # Gather Stuff
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            c_password = request.POST['c_password']
            
            if User.objects.filter(username__iexact=username).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Customer with this username Already Exists!'})
                messages.error(request, 'Error! Customer with this username Already Exists')
                return redirect('customer_new')
            if User.objects.filter(email__iexact=email).exists() and len(email):
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Customer with this email Already Exists!'})
                messages.error(request, 'Error! Customer with this email Already Exists')
                return redirect('customer_new')
            if password != c_password:
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Passwords are not matching!'})
                messages.error(request, 'Error! Passwords are not matching')
                return redirect('customer_new')

            customer = Customer()
            last_name = request.POST['last_name']
            first_name = request.POST['first_name']
            user = User.objects.create_user(
                        username=username,
                        password=password, email=email,
                        first_name=first_name, last_name=last_name
                    )
            user.save()
            customer.user = user
            customer.contact = request.POST['contact']
            # customer.organization = request.POST['organization']
            customer.address = request.POST['address']
            customer.country = request.POST['country']
            if 'state' in request.POST:
                customer.state = request.POST['state']
            if 'city' in request.POST:
                customer.city = request.POST['city']
            if 'is_available' in request.POST:
                customer.is_available = True
            customer.save()

            if "modal" in request.POST:
                queryset = Customer.objects.all().order_by('id').values(
                    'id', 'user'
                )

                return JsonResponse({'results': list(queryset),
                                     'status': 'customers',
                                     'selected': 'Select a Customer',
                                     'message': 'Customer is added successfully!'})

            messages.success(request, 'Success! Customer is saved')
            form = CustomerForm()

        context = {
            'form': form,
            'status': 'Add Customer',
            'page_name': 'Form',
            'list': False,
        }
        return render(request, 'pages/customer/customer.html', context)
    return render(request, 'accounts/login.html')

def customer_list(request):
    if request.user.is_authenticated:
        queryset = Customer.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Customers List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/customer/customer.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def customer_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Customer, id=id)

        context = {
            'obj': obj,
            'status': 'Customer Detail',
            'page_name': 'Detail',
            'list': False,
        }
        return render(request, 'pages/customer/customer.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def customer_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Customer, id=id)
        form = CustomerForm(initial={
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username,
            'email': obj.user.email,
            'contact': obj.contact,
            'address': obj.address,
            'city': obj.city,
            'state': obj.state,
            'country': obj.country,
            'date_added': obj.date_added,
            'is_available': obj.is_available,
        })
        
        if request.method == 'POST':
            # Gather Stuff
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            c_password = request.POST['c_password']

            if User.objects.filter(username__iexact=username).exclude(id=obj.user.id).exists():
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Customer with this username Already Exists!'})
                messages.error(
                    request, 'Error! Customer with this username Already Exists')
                return HttpResponseRedirect('/inventory/customer/update/%d/' % obj.id)
            if User.objects.filter(email__iexact=email).exclude(id=obj.user.id).exists() and len(email):
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Customer with this email Already Exists!'})
                messages.error(
                    request, 'Error! Customer with this email Already Exists')
                return HttpResponseRedirect('/inventory/customer/update/%d/' % obj.id)
            if password != c_password and len(password):
                if "modal" in request.POST:
                    return JsonResponse({'message': 'Passwords are not matching!'})
                messages.error(request, 'Error! Passwords are not matching')
                return HttpResponseRedirect('/inventory/customer/update/%d/' % obj.id)
            
            if len(password):
                obj.user.set_password(password)
            obj.user.username = username
            obj.user.email = email
            obj.user.first_name = request.POST['first_name']
            obj.user.last_name = request.POST['last_name']
            obj.user.save()
            obj.contact = request.POST['contact']
            # obj.organization = request.POST['organization']
            obj.address = request.POST['address']
            obj.country = request.POST['country']
            if 'state' in request.POST:
                obj.state = request.POST['state']
            if 'city' in request.POST:
                obj.city = request.POST['city']
            if 'is_available' in request.POST:
                obj.is_available = True
            else:
                obj.is_available = False
            obj.save()

            messages.success(
                request, f'Success! Customer "{obj.user.username}" is updated')
            return redirect('customer_list')

        context = {
            'form': form,
            'status': 'Update Customer',
            'page_name': 'Form',
            'list': False,
            'obj': obj,
        }
        return render(request, 'pages/customer/customer.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def customer_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Customer, id=id)
        obj.user.delete()
        messages.success(request, f'Success! Customer "{obj.user.username}" is Deleted')
        obj.delete()
        return redirect('customer_list')

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ CUSTOMER ++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ DEMAND ++++++++++++++++++++++++++

def demand_new(request):

    if request.user.is_authenticated:
        form = DemandForm(request.POST or None)
        if form.is_valid():

            items = []
            stocks = []
            demand = form.save(commit=False)
            demand.status = 'Pending'
            demand.date_added = getCurrentDate()
            demand.total_price = 0.0

            # Gather Items
            i = 0
            while i < int(request.POST['items_count']):
                if 'item'+str(i) in request.POST:
                    item = get_object_or_404(
                        Item, id=int(request.POST['item'+str(i)]))
                    if item.price is None:
                        messages.error(request, f'Error! Item "{item.name}" have no price')
                        return redirect('demand_new')
                    items.append(item)
                else:
                    i += 1
                    continue
                if 'stock'+str(i) in request.POST:
                    stock = int(request.POST['stock'+str(i)])
                    stocks.append(stock)
                demand.total_price += (item.price*stock)
                i += 1

            demand.save()

            if len(items)>0:
                di = Demand_Items()
                for i in range(len(items)):
                    di.demand = demand
                    di.item = items[i]
                    di.stock = stocks[i]
                di.save(force_insert=True)
            del items
            del stocks

            if "modal" in request.POST:
                queryset = Demand.objects.all().order_by('id').values(
                    'id', 'customer', 'date_added'
                )

                return JsonResponse({'results': list(queryset),
                                     'status': 'demands',
                                     'selected': 'Select a Demand',
                                     'message': 'Demand is added successfully!'})

            messages.success(request, 'Success! Demand is saved')
            form = DemandForm()

        context = {
            'form': form,
            'status': 'Add Demand',
            'page_name': 'Form',
            'list': False,
            'items': list(Item.objects.all().order_by('id').values('id', 'name')),
        }
        return render(request, 'pages/demand/demand.html', context)
    return render(request, 'accounts/login.html')

def demand_list(request):
    if request.user.is_authenticated:
        queryset = Demand.objects.all().order_by('id')
        context = {
            'data': queryset,
            'status': 'Demands List',
            'page_name': 'List',
            'list': True,
        }
        return render(request, 'pages/demand/demand.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def demand_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Demand, id=id)

        context = {
            'obj': obj,
            'status': 'Demand Detail',
            'page_name': 'Detail',
            'list': False,
            'demand_items': list(Demand_Items.objects.filter(demand=obj)),
        }
        return render(request, 'pages/demand/demand.html', context)

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def demand_update(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Demand, id=id)
        form = DemandForm(request.POST or None, instance=obj)
        demand_items = Demand_Items.objects.filter(demand=obj)

        if form.is_valid() and request.method == 'POST':
            items = []
            stocks = []
            form.save(commit=False)
            obj.total_price = 0.0

            # Gather Items
            i = 0
            while i < int(request.POST['items_count']):
                if 'item'+str(i) in request.POST:
                    item = get_object_or_404(
                        Item, id=int(request.POST['item'+str(i)]))
                    if item.price is None:
                        messages.error(
                            request, f'Error! Item "{item.name}" have no price')
                        return HttpResponseRedirect('/inventory/demand/update/%d/' % obj.id)
                    items.append(item)
                else:
                    i += 1
                    continue
                if 'stock'+str(i) in request.POST:
                    stock = int(request.POST['stock'+str(i)])
                    stocks.append(stock)
                obj.total_price += (item.price*stock)
                i += 1

            obj.save()
            demand_items.delete()

            if len(items) > 0:
                di = Demand_Items()
                for i in range(len(items)):
                    di.demand = obj
                    di.item = items[i]
                    di.stock = stocks[i]
                di.save(force_insert=True)
            del items
            del stocks

            messages.success(
                request, f'Success! Demand "{obj.customer} {obj.date_added}" is updated')
            return redirect('demand_list')

        context = {
            'form': form,
            'status': 'Update Demand',
            'page_name': 'Form',
            'list': False,
            'obj': obj,
            'demand_items': list(demand_items),
            'items': list(Item.objects.all().order_by('id').values('id', 'name')),
            'len': len(list(demand_items))+1,
        }
        return render(request, 'pages/demand/demand.html', context)
    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

def demand_delete(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Demand, id=id)

        Demand_Items.objects.filter(demand=obj).delete()
        messages.success(request, f'Success! Demand "{obj.customer} {obj.date_added}" is Deleted')
        obj.delete()
        return redirect('vendor_list')

    messages.error(request, 'Error! You Have to login First')
    return render(request, 'accounts/login.html')

# +++++++++++++++++++++++++++ DEMAND ++++++++++++++++++++++++++
