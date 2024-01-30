from django.shortcuts import render,redirect,get_object_or_404
from Register_Login.models import *
from Register_Login.views import logout
from . models import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
# Create your views here.



# -------------------------------Company section--------------------------------

# company dashboard
def company_dashboard(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
           
        else:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        context = {
            'details': dash_details,
            'allmodules': allmodules
        }
        return render(request, 'company/company_dash.html', context)
    else:
        return redirect('/')


# company profile
def company_profile(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
           
        else:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        
        context = {
            'details': dash_details,
            'allmodules': allmodules
        }
        return render(request, 'company/company_profile.html', context)
    else:
        return redirect('/')

# company profile
def company_staff_request(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
           
        else:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        staff_request=StaffDetails.objects.filter(company=dash_details.id, company_approval=0).order_by('-id')
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'requests':staff_request,
        }
        return render(request, 'company/staff_request.html', context)
    else:
        return redirect('/')

# company staff accept or reject
def staff_request_accept(request,pk):
    staff=StaffDetails.objects.get(id=pk)
    staff.company_approval=1
    staff.save()
    return redirect('company_staff_request')

def staff_request_reject(request,pk):
    staff=StaffDetails.objects.get(id=pk)
    login_details=LoginDetails.objects.get(id=staff.company.id)
    login_details.delete()
    staff.delete()
    return redirect('company_staff_request')


# All company staff view, cancel staff approval
def company_all_staff(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
           
        else:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        all_staffs=StaffDetails.objects.filter(company=dash_details.id, company_approval=1).order_by('-id')
        print(all_staffs)
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'staffs':all_staffs,
        }
        return render(request, 'company/all_staff_view.html', context)
    else:
        return redirect('/')

def staff_approval_cancel(request,pk):
    staff=StaffDetails.objects.get(id=pk)
    staff.company_approval=2
    staff.save()
    return redirect('company_all_staff')









# -------------------------------Staff section--------------------------------

# staff dashboard
def staff_dashboard(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
           
        else:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        context={
            'details':dash_details,
            'allmodules': allmodules,
        }
        return render(request,'staff/staff_dash.html',context)
    else:
        return redirect('/')


# staff profile
def staff_profile(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
           
        else:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        context={
            'details':dash_details,
            'allmodules': allmodules,
        }
        return render(request,'staff/staff_profile.html',context)
    else:
        return redirect('/')











# -------------------------------Zoho Modules section--------------------------------


#------------------- PRICE LIST MODULE ------------


#  display all price lists
def all_price_lists(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
        else:
            return redirect('/')
    log_details= LoginDetails.objects.get(id=log_id)
    if log_details.user_type=="Company":
        dash_details = CompanyDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        sort_option = request.GET.get('sort', 'all')  
        filter_option = request.GET.get('filter', 'all')
        if sort_option == 'name':
            price_lists = price_lists.order_by('name')
        elif sort_option == 'type':
            price_lists = price_lists.order_by('type')

        if filter_option == 'active':
            price_lists = price_lists.filter(status='Active')
        elif filter_option == 'inactive':
            price_lists = price_lists.filter(status='Inactive')
        context={
            'log_id':log_id,
            'log_details':log_details,
            'details':dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'sort_option': sort_option,
            'filter_option': filter_option,
        }
        return render(request,'zohomodules/price_list/all_price_lists.html',context)
    
    if log_details.user_type=="Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details.company)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        sort_option = request.GET.get('sort', 'all')  
        filter_option = request.GET.get('filter', 'all')
        if sort_option == 'name':
            price_lists = price_lists.order_by('name')
        elif sort_option == 'type':
            price_lists = price_lists.order_by('type')

        if filter_option == 'active':
            price_lists = price_lists.filter(status='Active')
        elif filter_option == 'inactive':
            price_lists = price_lists.filter(status='Inactive')
        context={
            'log_id':log_id,
            'log_details':log_details,
            'details':dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'sort_option': sort_option,
            'filter_option': filter_option,
        }
        return render(request,'zohomodules/price_list/all_price_lists.html',context)



import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PriceList, PriceListItem, PriceListTransactionHistory, CompanyDetails, LoginDetails

# def import_price_list(request):
#     if 'login_id' in request.session:
#         if request.session.has_key('login_id'):
#             log_id = request.session['login_id']
#         else:
#             return redirect('/')
    
#     log_details = LoginDetails.objects.get(id=log_id)

#     if log_details.user_type == "Company":
#         dash_details = CompanyDetails.objects.get(login_details=log_details)
#         items = Items.objects.filter(company=dash_details,activation_tag='active')
#         if request.method == 'POST' and request.FILES['file']:
#             csv_file = request.FILES['file']

#         try:
#             decoded_file = csv_file.read().decode('utf-8', errors='replace').splitlines()
#             reader = csv.DictReader(decoded_file)

            
#             for row in reader:
                
#                 new_price_list = PriceList.objects.create(
#                     name=row['NAME'],  
#                     type=row['TYPE'], 
#                     item_rate_type=row['ITEM_RATE_TYPE'],
#                     description=row['DESCRIPTION'],
#                     percentage_type=row['PERCENTAGE_TYPE'],
#                     percentage_value=row['PERCENTAGE_VALUE'],
#                     round_off=row['ROUND_OFF'],
#                     currency=row['CURRENCY'],
#                     company=dash_details,
#                     login_details=log_details,
#                 )
#                 PriceListTransactionHistory.objects.create(
#                 company=dash_details,
#                 login_details=log_details,
#                 price_list=new_price_list,
#                 action='Created',
#                 )
#                 custom_rates = request.POST.getlist('custom_rate')
#                 for item, custom_rate in zip(items, custom_rates):
#                     custom_rate = custom_rate if custom_rate else (item.selling_price if new_price_list.type == 'Sales' else item.purchase_price)
#                     standard_rate = item.selling_price if new_price_list.type == 'Sales' else item.purchase_price
#                     PriceListItem.objects.create(
#                         company=dash_details,
#                         login_details=log_details,
#                         price_list=new_price_list,
#                         item=item,
#                         standard_rate=standard_rate,
#                         custom_rate=custom_rate,
#                     )
#                 return redirect('all_price_lists')
#             context = {
#             'details': dash_details,
#             'items': items,
#             }
#             messages.success(request, 'Price List data imported successfully.')
#             return redirect('all_price_lists',context)


#         except Exception as e:
#             messages.error(request, f'Error importing data: {str(e)}')

#     elif log_details.user_type == "Staff":
#         dash_details = StaffDetails.objects.get(login_details=log_details)
#         if request.method == 'POST' and request.FILES['file']:
#             csv_file = request.FILES['file']

#         try:
#             decoded_file = csv_file.read().decode('utf-8').splitlines()
#             reader = csv.DictReader(decoded_file)
            
#             for row in reader:
#                 new_price_list = PriceList.objects.create(
#                     name=row['name'], 
#                     type=row['type'],  
#                     item_rate_type=row['item_rate_type'],
#                     description=row['description'],
#                     percentage_type=row['percentage_type'],
#                     percentage_value=row['percentage_value'],
#                     round_off=row['round_off'],
#                     currency=row['currency'],
#                     company=dash_details,
#                     login_details=log_details,
#                 )
#                 PriceListTransactionHistory.objects.create(
#                 company=dash_details,
#                 login_details=log_details,
#                 price_list=new_price_list,
#                 action='Created',
#                 )
#                 custom_rates = request.POST.getlist('custom_rate')
#                 for item, custom_rate in zip(items, custom_rates):
#                     custom_rate = custom_rate if custom_rate else (item.selling_price if new_price_list.type == 'Sales' else item.purchase_price)
#                     standard_rate = item.selling_price if new_price_list.type == 'Sales' else item.purchase_price
#                     PriceListItem.objects.create(
#                         company=dash_details,
#                         login_details=log_details,
#                         price_list=new_price_list,
#                         item=item,
#                         standard_rate=standard_rate,
#                         custom_rate=custom_rate,
#                     )
#                 return redirect('all_price_lists')
#             context = {
#             'details': dash_details,
#             'items': items,
#             }
#             messages.success(request, 'Price List data imported successfully.')
#             return redirect('all_price_lists',context)
#         except Exception as e:
#             messages.error(request, f'Error importing data: {str(e)}')
#     else:
#         return redirect('/')

    
#     return redirect('all_price_lists') 


# def import_price_list(request):
#     if 'login_id' in request.session:
#         if request.session.has_key('login_id'):
#             log_id = request.session['login_id']
#         else:
#             return redirect('/')
    
#     log_details = LoginDetails.objects.get(id=log_id)

#     if log_details.user_type == "Company":
#         dash_details = CompanyDetails.objects.get(login_details=log_details)
#         items = Items.objects.filter(company=dash_details, activation_tag='active')
#         if request.method == 'POST' and request.FILES['file']:
#             csv_file = request.FILES['file']

#             try:
#                 decoded_file = csv_file.read().decode('utf-8', errors='replace').splitlines()
#                 reader = csv.DictReader(decoded_file)

#                 for row in reader:
#                     new_price_list = PriceList.objects.create(
#                         name=row['NAME'],
#                         type=row['TYPE'],
#                         item_rate_type=row['ITEM_RATE_TYPE'],
#                         description=row['DESCRIPTION'],
#                         percentage_type=row['PERCENTAGE_TYPE'],
#                         percentage_value=row['PERCENTAGE_VALUE'],
#                         round_off=row['ROUNDINGL'],
#                         currency=row['CURRENCY'],
#                         company=dash_details,
#                         login_details=log_details,
#                     )
#                     PriceListTransactionHistory.objects.create(
#                         company=dash_details,
#                         login_details=log_details,
#                         price_list=new_price_list,
#                         action='Created',
#                     )
#                     custom_rates = request.POST.getlist('custom_rate')
#                     for item, custom_rate in zip(items, custom_rates):
#                         custom_rate = custom_rate if custom_rate else (item.selling_price if new_price_list.type == 'Sales' else item.purchase_price)
#                         standard_rate = item.selling_price if new_price_list.type == 'Sales' else item.purchase_price
#                         PriceListItem.objects.create(
#                             company=dash_details,
#                             login_details=log_details,
#                             price_list=new_price_list,
#                             item=item,
#                             standard_rate=standard_rate,
#                             custom_rate=custom_rate,
#                         )
#                     messages.success(request, 'Price List data imported successfully.')
#                     return redirect('all_price_lists')
                
#                 context = {
#                     'details': dash_details,
#                     'items': items,
#                 }
#                 messages.success(request, 'Price List data imported successfully.')
#                 return redirect('all_price_lists', context)

#             except Exception as e:
#                 messages.error(request, f'Error importing data: {str(e)}')

#     elif log_details.user_type == "Staff":
#         dash_details = StaffDetails.objects.get(login_details=log_details)
#         items = Items.objects.filter(company=dash_details, activation_tag='active')
#         if request.method == 'POST' and request.FILES['file']:
#             csv_file = request.FILES['file']

#             try:
#                 decoded_file = csv_file.read().decode('utf-8').splitlines()
#                 reader = csv.DictReader(decoded_file)

#                 for row in reader:
#                     new_price_list = PriceList.objects.create(
#                         name=row['NAME'],
#                         type=row['TYPE'],
#                         item_rate_type=row['ITEM_RATE_TYPE'],
#                         description=row['DESCRIPTION'],
#                         percentage_type=row['PERCENTAGE_TYPE'],
#                         percentage_value=row['PERCENTAGE_VALUE'],
#                         round_off=row['ROUNDINGL'],
#                         currency=row['CURRENCY'],
#                         company=dash_details,
#                         login_details=log_details,
#                     )
#                     PriceListTransactionHistory.objects.create(
#                         company=dash_details,
#                         login_details=log_details,
#                         price_list=new_price_list,
#                         action='Created',
#                     )
#                     custom_rates = request.POST.getlist('custom_rate')
#                     for item, custom_rate in zip(items, custom_rates):
#                         custom_rate = custom_rate if custom_rate else (item.selling_price if new_price_list.type == 'Sales' else item.purchase_price)
#                         standard_rate = item.selling_price if new_price_list.type == 'Sales' else item.purchase_price
#                         PriceListItem.objects.create(
#                             company=dash_details,
#                             login_details=log_details,
#                             price_list=new_price_list,
#                             item=item,
#                             standard_rate=standard_rate,
#                             custom_rate=custom_rate,
#                         )
#                     messages.success(request, 'Price List data imported successfully.')
#                     return redirect('all_price_lists')
                
#                 context = {
#                     'details': dash_details,
#                     'items': items,
#                 }
#                 messages.success(request, 'Price List data imported successfully.')
#                 return redirect('all_price_lists', context)

#             except Exception as e:
#                 messages.error(request, f'Error importing data: {str(e)}')

#     else:
#         return redirect('/')

#     return redirect('all_price_lists')

from django.shortcuts import redirect
from django.contrib import messages
from .models import PriceList, PriceListTransactionHistory, PriceListItem
from Register_Login.models import LoginDetails, CompanyDetails, StaffDetails
import csv

import pandas as pd
from django.contrib import messages
from .models import PriceList, PriceListItem, PriceListTransactionHistory, Items

# def import_price_list(request):
#     if 'login_id' in request.session:
#         if request.session.has_key('login_id'):
#             log_id = request.session['login_id']
#         else:
#             return redirect('/')
    
#     log_details = LoginDetails.objects.get(id=log_id)

#     if log_details.user_type == "Company":
#         dash_details = CompanyDetails.objects.get(login_details=log_details)

#         if request.method == 'POST' and request.FILES.get('price_list_file') and request.FILES.get('items_file'):
#             price_list_file = request.FILES['price_list_file']
#             items_file = request.FILES['items_file']

#             try:
#                 # Read PriceList Excel file
#                 price_list_df = pd.read_excel(price_list_file)

#                 # Create PriceList and PriceListItem instances
#                 for index, row in price_list_df.iterrows():
#                     new_price_list = PriceList.objects.create(
#                         name=row['NAME'],
#                         type=row['TYPE'],
#                         item_rate_type=row['TYPE'],
#                         description=row['DESCRIPTION'],
#                         percentage_type=row['PERCENTAGE_TYPE'],
#                         percentage_value=row['PERCENTAGE_VALUE'],
#                         round_off=row['ROUNDING'],
#                         currency=row['CURRENCY'],
#                         company=dash_details,
#                         login_details=log_details,
#                     )
#                     PriceListTransactionHistory.objects.create(
#                         company=dash_details,
#                         login_details=log_details,
#                         price_list=new_price_list,
#                         action='Created',
#                     )

#                     # Read Items Excel file for each PriceList
#                     items_df = pd.read_excel(items_file)

#                     # Create PriceListItem instances
#                     for item_index, item_row in items_df.iterrows():
#                         item = Items.objects.get(item_name=item_row['ITEM_NAME'], company=dash_details)
#                         custom_rate = item_row.get('CUSTOM_RATE', item.selling_price if new_price_list.type == 'Sales' else item.purchase_price)
#                         standard_rate = item.selling_price if new_price_list.type == 'Sales' else item.purchase_price
#                         PriceListItem.objects.create(
#                             company=dash_details,
#                             login_details=log_details,
#                             price_list=new_price_list,
#                             item=item,
#                             standard_rate=standard_rate,
#                             custom_rate=custom_rate,
#                         )

#                 messages.success(request, 'Price List data imported successfully.')
#                 return redirect('all_price_lists')

#             except Exception as e:
#                 messages.error(request, f'Error importing data: {str(e)}')

#     # elif log_details.user_type == "Staff":
#         # ... (similar code for Staff user)
    
        

#     else:
#         return redirect('/')

#     return redirect('all_price_lists')

def import_price_list(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
        else:
            return redirect('/')
    
    log_details = LoginDetails.objects.get(id=log_id)

    if log_details.user_type == "Company":
        dash_details = CompanyDetails.objects.get(login_details=log_details)

        if request.method == 'POST' and request.FILES.get('price_list_file') and request.FILES.get('items_file'):
            price_list_file = request.FILES['price_list_file']
            items_file = request.FILES['items_file']

            try:
                # Read PriceList Excel file(price_list_file)
                price_list_df = pd.read_excel(price_list_file)

                # Create PriceList and PriceListItem instances
                for index, row in price_list_df.iterrows():
                    # Check if a PriceList with the same name already exists
                    existing_price_list = PriceList.objects.filter(name=row['NAME'], company=dash_details).first()
                    if existing_price_list:
                        messages.error(request, f'Error importing data: PriceList with name "{row["NAME"]}" already exists.')
                        continue

                    new_price_list = PriceList.objects.create(
                        name=row['NAME'],
                        type=row['TYPE'],
                        item_rate_type=row['ITEM_RATE_TYPE'], 
                        description=row['DESCRIPTION'],
                        percentage_type=row['PERCENTAGE_TYPE'],
                        percentage_value=row['PERCENTAGE_VALUE'],
                        round_off=row['ROUNDING'],
                        currency=row['CURRENCY'],
                        company=dash_details, 
                        login_details=log_details,
                    )
                    PriceListTransactionHistory.objects.create(
                        company=dash_details,
                        login_details=log_details,
                        price_list=new_price_list,
                        action='Created',
                    )

                    # Read Items Excel file(items_file) for each PriceList
                    items_df = pd.read_excel(items_file)

                    # Create PriceListItem instances for active items only
                    for item_index, item_row in items_df.iterrows():
                        item = Items.objects.filter(item_name=item_row['ITEM_NAME'], company=dash_details, activation_tag='active').first()
                        if item:
                            # Use custom rate if available, otherwise use the standard rate of the item
                            # custom_rate = item_row.get('CUSTOM_RATE', item.selling_price if new_price_list.type == 'Sales' else item.purchase_price)
                            # custom_rate1 = item_row['SELLING_CUSTOM_RATE'] if new_price_list.type == 'Sales' else standard_rate, item_row['PURCHASE_CUSTOM_RATE'] if new_price_list.type == 'Purchase' else standard_rate
                            
                            # standard_rate = item.selling_price if new_price_list.type == 'Sales' else item.purchase_price
                            # custom_rate1 = item_row.get('SELLING_CUSTOM_RATE',item.selling_price if new_price_list.type == 'Sales' else  'PURCHASE_CUSTOM_RATE',item.purchase_price )
                            # custom_rate = standard_rate if new_price_list.item_rate_type == 'Percentage' else custom_rate1
                            
                            standard_rate = item.selling_price if new_price_list.type == 'Sales' else item.purchase_price
                            standard_rate1 = item.selling_price if new_price_list.type == 'Sales' else item.purchase_price
                            custom_rate1 = item_row.get('SELLING_CUSTOM_RATE', standard_rate1) if new_price_list.type == 'Sales' else item_row.get('PURCHASE_CUSTOM_RATE', standard_rate1)
                            custom_rate = standard_rate if new_price_list.item_rate_type == 'Percentage' else custom_rate1


                            
                            
                            PriceListItem.objects.create(
                                company=dash_details,
                                login_details=log_details,
                                price_list=new_price_list,
                                item=item,
                                standard_rate=standard_rate,
                                custom_rate=custom_rate,
                            )
                        else:
                            messages.warning(request, f'Skipping item "{item_row["ITEM_NAME"]}" in PriceList "{row["NAME"]}": Item is not active.')

                messages.success(request, 'Price List data imported successfully.')
                return redirect('all_price_lists')

            except Exception as e:
                messages.error(request, f'Error importing data: {str(e)}')

    else:
        return redirect('/')

    return redirect('all_price_lists')

def create_price_list(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
        else:
            return redirect('/')
    
    log_details = LoginDetails.objects.get(id=log_id)

    if log_details.user_type == "Company":
        dash_details = CompanyDetails.objects.get(login_details=log_details)
        allmodules = ZohoModules.objects.get(company=dash_details, status='New')
        items = Items.objects.filter(company=dash_details,activation_tag='active')

        if request.method == 'POST':
            name = request.POST['name']
            if PriceList.objects.filter(name=name, company=dash_details).exists():
                messages.error(request, f"A Price List with the name '{name}' already exists.")
                return redirect('create_price_list')
            
            new_price_list = PriceList.objects.create(
                name=name,
                type=request.POST['type'],
                item_rate_type=request.POST['item_rate_type'],
                description=request.POST['description'],
                percentage_type=request.POST['percentage_type'],
                percentage_value=request.POST['percentage_value'],
                round_off=request.POST['round_off'],
                currency=request.POST['currency'],
                company=dash_details,
                login_details=log_details,
            )

            PriceListTransactionHistory.objects.create(
                company=dash_details,
                login_details=log_details,
                price_list=new_price_list,
                action='Created',
            )
            custom_rates = request.POST.getlist('custom_rate')
            for item, custom_rate in zip(items, custom_rates):
                custom_rate = custom_rate if custom_rate else (item.selling_price if new_price_list.type == 'Sales' else item.purchase_price)
                standard_rate = item.selling_price if new_price_list.type == 'Sales' else item.purchase_price
                PriceListItem.objects.create(
                    company=dash_details,
                    login_details=log_details,
                    price_list=new_price_list,
                    item=item,
                    standard_rate=standard_rate,
                    custom_rate=custom_rate,
                )
            return redirect('all_price_lists')
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'items': items,
        }
        return render(request, 'zohomodules/price_list/create_price_list.html', context)

    if log_details.user_type == "Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
        items = Items.objects.filter(company=dash_details.company,activation_tag='active')

        if request.method == 'POST':
            name = request.POST['name']
            if PriceList.objects.filter(name=name, company=dash_details.company).exists():
                messages.error(request, f"A Price List with the name '{name}' already exists.")
                return redirect('create_price_list')
            
            new_price_list = PriceList.objects.create(
                name=name,
                type=request.POST['type'],
                item_rate_type=request.POST['item_rate_type'],
                description=request.POST['description'],
                percentage_type=request.POST['percentage_type'],
                percentage_value=request.POST['percentage_value'],
                round_off=request.POST['round_off'],
                currency=request.POST['currency'],
                company=dash_details.company,
                login_details=log_details
            )
            
            PriceListTransactionHistory.objects.create(
                company=dash_details.company,
                login_details=log_details,
                price_list=new_price_list,
                action='Created',
            )
            
            custom_rates = request.POST.getlist('custom_rate')
            for item, custom_rate in zip(items, custom_rates):
                custom_rate = custom_rate if custom_rate else (item.selling_price if new_price_list.type == 'Sales' else item.purchase_price)
                standard_rate = item.selling_price if new_price_list.type == 'Sales' else item.purchase_price
                PriceListItem.objects.create(
                    company=dash_details.company,
                    login_details=log_details,
                    price_list=new_price_list,
                    item=item,
                    standard_rate=standard_rate,
                    custom_rate=custom_rate,
                )

            return redirect('all_price_lists')

        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'items': items,
        }
        return render(request, 'zohomodules/price_list/create_price_list.html', context)
 

def edit_price_list(request, price_list_id):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
        else:
            return redirect('/')
    log_details = LoginDetails.objects.get(id=log_id)
    if log_details.user_type == "Company":
        dash_details = CompanyDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details)
        allmodules = ZohoModules.objects.get(company=dash_details, status='New')
        price_list = get_object_or_404(PriceList, id=price_list_id)
        items = PriceListItem.objects.filter(price_list=price_list)

        
        if request.method == 'POST':
            price_list.name = request.POST['name']
            price_list.type = request.POST['type']
            price_list.item_rate_type = request.POST['item_rate_type']
            price_list.description = request.POST['description']
            price_list.percentage_type = request.POST['percentage_type']
            price_list.percentage_value = request.POST['percentage_value']
            price_list.round_off = request.POST['round_off']
            price_list.currency = request.POST['currency']
            price_list.save()
            
            PriceListTransactionHistory.objects.create(
                company=dash_details,
                login_details=log_details,
                price_list=price_list,
                action='Edited',
            )
            
            # edit PriceListItem
            custom_rate = request.POST.getlist('custom_rate')
            items = PriceListItem.objects.filter(price_list=price_list)
            for item, custom_rate in zip(items, custom_rate):
                standard_rate = item.item.selling_price if price_list.type == 'Sales' else item.item.purchase_price
                item.standard_rate = standard_rate
                item.custom_rate = custom_rate
                item.save()
            
            
            return redirect('all_price_lists')
        context = {
            'log_details': log_details,
            'details': dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'price_list': price_list,
            'items': items,
        }
        return render(request, 'zohomodules/price_list/edit_price_list.html', context)
    elif log_details.user_type == "Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details.company)
        allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
        price_list = get_object_or_404(PriceList, id=price_list_id)
        items = PriceListItem.objects.filter(price_list=price_list)
        
        if request.method == 'POST':
            price_list.name = request.POST['name']
            price_list.type = request.POST['type']
            price_list.item_rate_type = request.POST['item_rate_type']
            price_list.description = request.POST['description']
            price_list.percentage_type = request.POST['percentage_type']
            price_list.percentage_value = request.POST['percentage_value']
            price_list.round_off = request.POST['round_off']
            price_list.currency = request.POST['currency']
            price_list.save()
            PriceListTransactionHistory.objects.create(
                    company=dash_details.company,
                    login_details=log_details,
                    price_list=price_list,
                    action='Edited',
                )
            
            # edit PriceListItem
            custom_rate = request.POST.getlist('custom_rate')
            for item, custom_rate in zip(items, custom_rate):
                    standard_rate = item.item.selling_price if price_list.type == 'Sales' else item.item.purchase_price
                    item.standard_rate = standard_rate
                    item.custom_rate = custom_rate
                    item.save()
            
            return redirect('all_price_lists')

        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'price_list': price_list,
            'items':items,
        }
        return render(request, 'zohomodules/price_list/edit_price_list.html', context)


# display details of selected price list
def price_list_details(request, price_list_id):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
        else:
            return redirect('/')
    log_details= LoginDetails.objects.get(id=log_id)
    
    if log_details.user_type=="Company":
        dash_details = CompanyDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details)
        price_list = get_object_or_404(PriceList, id=price_list_id)
        comments = PriceListComment.objects.filter(price_list=price_list)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        sort_option = request.GET.get('sort', 'all')  
        filter_option = request.GET.get('filter', 'all')
        if sort_option == 'name':
            price_lists = price_lists.order_by('name')
        elif sort_option == 'type':
            price_lists = price_lists.order_by('type')

        if filter_option == 'active':
            price_lists = price_lists.filter(status='Active')
        elif filter_option == 'inactive':
            price_lists = price_lists.filter(status='Inactive')
        transaction_history = PriceListTransactionHistory.objects.filter(price_list=price_list)
        items = PriceListItem.objects.filter(company=dash_details, price_list=price_list)
        latest_transaction = PriceListTransactionHistory.objects.filter(price_list=price_list)

        context={
            'log_id':log_id,
            'log_details':log_details,
            'details':dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'price_list': price_list,
            'comments': comments,
            'sort_option': sort_option,
            'filter_option': filter_option,
            'latest_transaction': latest_transaction,
            'transaction_history': transaction_history,
            'items':items,
        }
        return render(request,'zohomodules/price_list/price_list_details.html',context)
    
    if log_details.user_type=="Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details.company)
        price_list = get_object_or_404(PriceList, id=price_list_id)
        comments = PriceListComment.objects.filter(price_list=price_list)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        sort_option = request.GET.get('sort', 'all')  
        filter_option = request.GET.get('filter', 'all')
        if sort_option == 'name':
            price_lists = price_lists.order_by('name')
        elif sort_option == 'type':
            price_lists = price_lists.order_by('type')

        if filter_option == 'active':
            price_lists = price_lists.filter(status='Active')
        elif filter_option == 'inactive':
            price_lists = price_lists.filter(status='Inactive')
        transaction_history = PriceListTransactionHistory.objects.filter(price_list=price_list)
        items = PriceListItem.objects.filter(company=dash_details.company, price_list=price_list)
        context={
            'log_id':log_id,
            'log_details':log_details,
            'details':dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'comments': comments,
            'price_list': price_list,
            'sort_option': sort_option,
            'filter_option': filter_option,
            'transaction_history': transaction_history,
            'items':items,
        }
        return render(request,'zohomodules/price_list/price_list_details.html',context)
    

def delete_price_list(request, price_list_id):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
        else:
            return redirect('/')
    log_details= LoginDetails.objects.get(id=log_id)
    if log_details.user_type=="Company":
        dash_details = CompanyDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details)
        price_list = get_object_or_404(PriceList, id=price_list_id)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        price_list.delete()
        context={
            'details':dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'price_list': price_list,
        }
        return render(request,'zohomodules/price_list/all_price_lists.html',context)
    if log_details.user_type=="Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details.company)
        price_list = get_object_or_404(PriceList, id=price_list_id)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        price_list.delete()
        context={
            'details':dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'price_list': price_list,
        }
        return render(request,'zohomodules/price_list/all_price_lists.html',context)


def toggle_price_list_status(request, price_list_id):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
        else:
            return redirect('/')
    log_details = LoginDetails.objects.get(id=log_id)
    if log_details.user_type == "Company":
        dash_details = CompanyDetails.objects.get(login_details=log_details)
        price_list = get_object_or_404(PriceList, id=price_list_id, company=dash_details)
        if price_list.status == 'Active':
            price_list.status = 'Inactive'
        else:
            price_list.status = 'Active'
        price_list.save()
        PriceListTransactionHistory.objects.create(
            company=dash_details,
            login_details=log_details,
            price_list=price_list,
            action='Edited' 
        )
        return redirect('price_list_details', price_list_id=price_list_id)
    if log_details.user_type == "Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        price_list = get_object_or_404(PriceList, id=price_list_id, company=dash_details.company)
        if price_list.status == 'Active':
            price_list.status = 'Inactive'
        else:
            price_list.status = 'Active'
        price_list.save()
        PriceListTransactionHistory.objects.create(
            company=dash_details.company,
            login_details=log_details,
            price_list=price_list,
            action='Edited'  
        )
        return redirect('price_list_details', price_list_id=price_list_id)

def add_comment(request, price_list_id):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
        else:
            return redirect('/')
    log_details = LoginDetails.objects.get(id=log_id)
    if log_details.user_type == "Company":
        dash_details = CompanyDetails.objects.get(login_details=log_details)
        price_list = get_object_or_404(PriceList, id=price_list_id, company=dash_details)
        if request.method == 'POST':
            comment = request.POST.get('comment_text')
            PriceListComment.objects.create(
                company=dash_details,
                login_details=log_details,
                price_list=price_list,
                comment=comment
            )
            
        return redirect('price_list_details', price_list_id=price_list_id)
    if log_details.user_type == "Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        price_list = get_object_or_404(PriceList, id=price_list_id, company=dash_details.company)
        if request.method == 'POST':
            comment = request.POST.get('comment_text')
            PriceListComment.objects.create(
                company=dash_details.company,
                login_details=log_details,
                price_list=price_list,
                comment=comment
            )
        return redirect('price_list_details', price_list_id=price_list_id)

def delete_comment(request, comment_id, price_list_id):
    comment = get_object_or_404(PriceListComment, id=comment_id)
    comment.delete()
    return redirect('price_list_details', price_list_id=price_list_id)



# def view_comment(request, price_list_id):
#     if 'login_id' in request.session:
#         if request.session.has_key('login_id'):
#             log_id = request.session['login_id']
#         else:
#             return redirect('/')
#     log_details = LoginDetails.objects.get(id=log_id)
    
#     if log_details.user_type == "Company":
#         dash_details = CompanyDetails.objects.get(login_details=log_details)
#         price_lists = PriceList.objects.filter(company=dash_details)
#         price_list = get_object_or_404(PriceList, id=price_list_id)
#         comments = PriceListComment.objects.filter(price_list=price_list)
#         context = {
#             'details': dash_details,
#             'price_lists': price_lists,
#             'price_list': price_list,
#             'comments': comments,
#         }
#         return render(request, 'zohomodules/price_list/price_list_details.html', context)

#     if log_details.user_type == "Staff":
#         dash_details = StaffDetails.objects.get(login_details=log_details)
#         price_list = get_object_or_404(PriceList, id=price_list_id, company=dash_details.company)
#         comments = PriceListComment.objects.filter(price_list=price_list)
#         context = {
#             'details': dash_details,
#             'price_list': price_list,
#             'comments': comments,
#         }
#         return render(request, 'zohomodules/price_list/price_list_details.html', context)




from django.shortcuts import render, redirect
from django.contrib import messages
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import PriceList, PriceListItem
import os

def whatsapp_pricelist(request, price_list_id):
    try:
        price_list = PriceList.objects.get(id=price_list_id)
        price_list_items = PriceListItem.objects.filter(price_list=price_list)

        context = {
            'price_list': price_list,
            'price_list_items': price_list_items,
        }

        # Render the template
        html = render(request, 'zohomodules/price_list/pdf_price_list.html', context).content

        # Create a PDF file
        pdf_file = BytesIO()
        pisa.pisaDocument(BytesIO(html), pdf_file)

        # Check if PDF generation was successful
        if pdf_file.tell():
            pdf_file.seek(0)

            # Save the PDF to the server's media folder
            pdf_filename = f"{price_list.name}_price_list.pdf"
            pdf_path = os.path.join('media', pdf_filename)
            with open(pdf_path, 'wb') as pdf_file_on_server:
                pdf_file_on_server.write(pdf_file.read())

            # Create a direct link to the saved PDF
            pdf_link = f"{request.scheme}://{request.get_host()}/{pdf_path}"

            # Create the WhatsApp message with a link to download the PDF
            whatsapp_message = f"Check out this price list: [Download PDF]{pdf_link}"

            # Create the WhatsApp link
            whatsapp_link = f"https://wa.me/?text={whatsapp_message}"

            # Return the WhatsApp link
            return redirect(whatsapp_link)

    except Exception as e:
        print(e)
        messages.error(request, f'{e}')

    # If there is an error or PDF generation fails, redirect to 'all_price_lists'
    return redirect('all_price_lists')


# from django.shortcuts import render, HttpResponse
# from django.template.loader import render_to_string
# from xhtml2pdf import pisa

# def generate_pdf(request, price_list_id):
#     price_list = PriceList.objects.get(id=price_list_id)
#     price_list_items = PriceListItem.objects.filter(price_list=price_list)

#         context = {
#             'price_list': price_list,
#             'price_list_items': price_list_items,
#         }
#     html = render_to_string('your_template_with_details_container.html', context)

#     # Create a PDF file
#     pdf_file = BytesIO()
#     pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf_file)

#     # Check if PDF generation was successful
#     if pdf_file.tell():
#         pdf_file.seek(0)

#         # Save the PDF file or serve it directly
#         # For simplicity, you can save it to the media directory
#         pdf_path = f'media/{price_list.name}_price_list.pdf'
#         with open(pdf_path, 'wb') as pdf:
#             pdf.write(pdf_file.read())

#         return HttpResponse(pdf_path)
#     else:
#         return HttpResponse("Error generating PDF", status=500)



# email pricelist details(overview)
def email_pricelist(request, price_list_id):
    try:
        price_list = PriceList.objects.get(id=price_list_id)
        price_list_item = PriceListItem.objects.filter( price_list=price_list)

        if request.method == 'POST':
            emails_string = request.POST['email_ids']
            emails_list = [email.strip() for email in emails_string.split(',')]
            email_message = request.POST['email_message']

            context = {
                'price_list': price_list,
                'price_list_item': price_list_item,
            }

            template_path = 'zohomodules/price_list/pdf_price_list.html'
            template = get_template(template_path)
            html = template.render(context)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            pdf = result.getvalue()

            filename = f'Price_List_Details.pdf'
            subject = f"Price List Details: {price_list.name}"
            email = EmailMessage(subject, f"Hi,\nPlease find the attached Price List Details. \n{email_message}\n\n--\nRegards,\n{price_list.name}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
            email.attach(filename, pdf, "application/pdf")
            email.send(fail_silently=False)

            msg = messages.success(request, 'Details have been shared via email successfully..!')
            return redirect('price_list_details', price_list_id=price_list_id)  

    except Exception as e:
        print(e)
        messages.error(request, f'{e}')
        return redirect('all_price_lists')  

# dwnld pdf
def price_list_pdf(request, price_list_id):
    try:
        price_list = PriceList.objects.get(id=price_list_id)
        price_list_item = PriceListItem.objects.filter(price_list=price_list)

        context = {
            'price_list': price_list,
            'price_list_item': price_list_item,
        }

        template_path = 'zohomodules/price_list/pdf_price_list.html'
        template = get_template(template_path)
        html = template.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        pdf = result.getvalue()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{price_list.name}_Details.pdf"'
        response.write(pdf)
        return response
    except Exception as e:
        print(e)
        messages.error(request, f'{e}')
        return redirect('all_price_lists')

# upload and download attachment
def attach_file(request, price_list_id):
    price_list = PriceList.objects.get(pk=price_list_id)
    if request.method == 'POST':
        attachment = request.FILES.get('attachment')
        price_list.attachment = attachment
        price_list.save()
        return redirect('price_list_details', price_list_id=price_list.id)
    return HttpResponse("Invalid request method.")













    
    
    
    
    
# email listout page
def email_all_price_lists(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
        else:
            return redirect('/')

        log_details = LoginDetails.objects.get(id=log_id)
        if log_details.user_type == "Company":
            dash_details = CompanyDetails.objects.get(login_details=log_details)
            price_lists = PriceList.objects.filter(company=dash_details)

            if request.method == 'POST':
                emails_string = request.POST['email_ids']
                emails_list = [email.strip() for email in emails_string.split(',')]
                email_message = request.POST['email_message']

                # Generate pdf content from HTML template
                template_path = 'zohomodules/price_list/pdf_all_price_lists.html'
                context = {
                    'price_lists': price_lists,
                    'dash_details':dash_details
                    }
                html_content = get_template(template_path).render(context)

                # Create BytesIO object and convert HTML to pdf
                pdf_file = BytesIO()
                pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), pdf_file)

                # Move the BytesIO pointer to the beginning
                pdf_file.seek(0)

                # Send email with pdf attachment
                filename = 'All_Price_Lists.pdf'
                subject = 'All_Price_Lists'
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Price Lists. \n{email_message}\n\n--\nRegards,\n{dash_details.company_name}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf_file.read(), "application/pdf")
                email.send(fail_silently=False)

                msg = messages.success(request, 'Details have been shared via email successfully..!')
                return redirect('all_price_lists')

            context = {
                'dash_details': dash_details,
                'price_lists': price_lists,
                'sort_option': 'all',
                'filter_option': 'all',
            }
            return render(request, 'zohomodules/price_list/all_price_lists.html', context)

        elif log_details.user_type == "Staff":
            dash_details = StaffDetails.objects.get(login_details=log_details)
            price_lists = PriceList.objects.filter(company=dash_details.company)

            if request.method == 'POST':
                emails_string = request.POST['email_ids']
                emails_list = [email.strip() for email in emails_string.split(',')]
                email_message = request.POST['email_message']

                # Generate pdf content from HTML template
                template_path = 'zohomodules/price_list/pdf_all_price_lists.html'
                context = {
                    'price_lists': price_lists,
                    'dash_details':dash_details
                    }
                html_content = get_template(template_path).render(context)

                # Create BytesIO object and convert HTML to pdf
                pdf_file = BytesIO()
                pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), pdf_file)
                pdf_file.seek(0)

                # Send email with pdf attachment
                filename = 'All_Price_Lists.pdf'
                subject = 'All_Price_Lists'
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Price Lists. \n{email_message}\n\n--\nRegards,\n{dash_details.company.company_name}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf_file.read(), "application/pdf")
                email.send(fail_silently=False)

                msg = messages.success(request, 'Details have been shared via email successfully..!')
                return redirect('all_price_lists')

            context = {
                'dash_details': dash_details,
                'price_lists': price_lists,
                'sort_option': 'all',
                'filter_option': 'all',
            }
            return render(request, 'zohomodules/price_list/all_price_lists.html', context)
        else:
            return HttpResponse("Unauthorized Access")

    else:
        return HttpResponse("Unauthorized Access")
  