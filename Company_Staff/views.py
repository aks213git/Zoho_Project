from django.shortcuts import render,redirect,get_object_or_404
from Register_Login.models import *
from Register_Login.views import logout
from . models import *

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
    price_lists = PriceList.objects.all()

    sortBy = request.GET.get('sortBy')
    filterByStatus = request.GET.get('filterByStatus')

    if sortBy == 'name':
        price_lists = price_lists.order_by('name')
    elif sortBy == 'type':
        price_lists = price_lists.order_by('type')

    if filterByStatus == 'active':
        price_lists = price_lists.filter(status='active')
    elif filterByStatus == 'inactive':
        price_lists = price_lists.filter(status='inactive')

    context = {'price_lists': price_lists}
    return render(request, 'zohomodules/all_price_lists.html', context)
# def all_price_lists(request):
#     if 'login_id' in request.session:
#         log_id = request.session['login_id']
#         if 'login_id' not in request.session:
#             return redirect('/')
#         elif
#             log_details=LoginDetails.objects.get(id=log_id)

#             details=StaffDetails.objects.get(LoginDetails=log_details)
#             allmodules= ZohoModules.objects.get(CompanyDetails.company)
    
# if 'login_id' in request.session:
#         log_id = request.session['login_id']
#         if 'login_id' not in request.session:
#             return redirect('/')

# log_details=LoginDetails.objects.get(id=log_id)
# # if staff
# details=StaffDetails.objects.get(LoginDetails=log_details)
# allmodules= ZohoModules.objects.get(CompanyDetails.company)
# # if company
# details=CompanyDetails.objects.get(LoginDetails=log_details)
# allmodules= ZohoModules.objects.get(company=details)


def create_price_list(request):
    login_id = request.session.get('login_id')
    log_user = LoginDetails.objects.get(id=login_id)
    if log_user.user_type == 'Company':
        company_details = CompanyDetails.objects.get(login_details=log_user)
        items = Items.objects.all() 

        if request.method == 'POST':
            new_price_list = PriceList.objects.create(
                name=request.POST['name'],
                type=request.POST['type'],
                item_rate_type=request.POST['item_rate_type'],
                description=request.POST['description'],
                percentage_type=request.POST['percentage_type'],
                percentage_value=request.POST['percentage_value'],
                round_off=request.POST['round_off'],
                currency=request.POST['currency'],
                company=company_details,
                login_details=log_user
            )

            items_data = request.POST.getlist('items')
            for item_data in items_data:
                item_id, custom_rate = map(int, item_data.split('-'))
                item = get_object_or_404(Items, id=item_id)
                PriceListItem.objects.create(
                    company=company_details,
                    login_details=log_user,
                    price_list=new_price_list,
                    item=item,
                    standard_rate=item.selling_price,
                    custom_rate=custom_rate
                )

            return redirect('all_price_lists')  
        log_details= LoginDetails.objects.get(id=login_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        
        context = {
            'company_details': company_details, 
            'items': items,
            'dash_details': dash_details,
            'allmodules': allmodules
            }
        return render(request, 'zohomodules/create_price_list.html', context)

    elif log_user.user_type == 'Staff':
        staff_details = StaffDetails.objects.get(login_details=log_user)
        items = Items.objects.all() 

        if request.method == 'POST':
            new_price_list = PriceList.objects.create(
                name=request.POST['name'],
                type=request.POST['type'],
                item_rate_type=request.POST['item_rate_type'],
                description=request.POST['description'],
                percentage_type=request.POST['percentage_type'],
                percentage_value=request.POST['percentage_value'],
                round_off=request.POST['round_off'],
                currency=request.POST['currency'],
                company=staff_details.company,  
                login_details=log_user
            )

            items_data = request.POST.getlist('items')
            for item_data in items_data:
                item_id, custom_rate = map(int, item_data.split('-'))
                item = get_object_or_404(Items, id=item_id)
                PriceListItem.objects.create(
                    company=staff_details.company,
                    login_details=log_user,
                    price_list=new_price_list,
                    item=item,
                    standard_rate=item.selling_price,
                    custom_rate=custom_rate
                )
            return redirect('all_price_lists')  
        log_details= LoginDetails.objects.get(id=login_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')

        context = {
            'staff_details': staff_details, 
            'items': items,
            'dash_details': dash_details,
            'allmodules': allmodules
            }
        return render(request, 'zohomodules/staff_create_price_list.html', context)
    
    else:
        return redirect('/') 


# display details of selected price list
def price_list_details(request, price_list_id):
    login_id = request.session.get('login_id')
    log_user = LoginDetails.objects.get(id=login_id)
    price_list = get_object_or_404(PriceList, id=price_list_id)
    price_list_items = PriceListItem.objects.filter(price_list=price_list)
    transaction_history = PriceListTransactionHistory.objects.filter(price_list=price_list)

    all_price_lists = PriceList.objects.filter(company=price_list.company)
    
    log_details= LoginDetails.objects.get(id=login_id)
    dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
    allmodules= ZohoModules.objects.get(company=dash_details,status='New')

    context = {
        'price_list': price_list,
        'price_list_items': price_list_items,
        'transaction_history': transaction_history,
        'all_price_lists': all_price_lists, 
        'allmodules': allmodules, 
        
    }

    return render(request, 'zohomodules/price_list_details.html', context)


# edit a price list
def edit_price_list(request, price_list_id):
    price_list = get_object_or_404(PriceList, id=price_list_id)

    if request.method == 'POST':
        price_list.name = request.POST['name']
        price_list.type = request.POST['type']
        
        price_list.save()
        return redirect('price_list_details', price_list_id=price_list.id)

    else:
        context = {'price_list': price_list}
        return render(request, 'edit_price_list.html', context)


def delete_price_list(request, price_list_id):
    price_list = get_object_or_404(PriceList, id=price_list_id)


def toggle_price_list_status(request, price_list_id):
    price_list = get_object_or_404(PriceList, id=price_list_id)




