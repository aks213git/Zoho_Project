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
        context={
            'details':dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
        }
        return render(request,'zohomodules/price_list/all_price_lists.html',context)
    
    if log_details.user_type=="Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details.company)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
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
        context={
            'details':dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
        }
        return render(request,'zohomodules/price_list/all_price_lists.html',context)

def create_price_list(request):
    if 'login_id' in request.session:
        if request.session.has_key('login_id'):
            log_id = request.session['login_id']
        else:
            return redirect('/')
    log_details= LoginDetails.objects.get(id=log_id)
    if log_details.user_type=="Company":
        dash_details = CompanyDetails.objects.get(login_details=log_details)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
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
                company=dash_details,
                login_details=log_details,
                )

            items_data = request.POST.getlist('items')
            for item_data in items_data:
                item_id, custom_rate = map(int, item_data.split('-'))
                item = get_object_or_404(Items, id=item_id)
                PriceListItem.objects.create(
                    price_list=new_price_list,
                    item=item,
                    standard_rate=item.selling_price,
                    custom_rate=custom_rate,
                    company=dash_details,
                    login_details=log_details,
                    
                )

            return redirect('all_price_lists')
        context={
            'details':dash_details,
            'allmodules': allmodules,

        }
        return render(request,'zohomodules/price_list/create_price_list.html',context)
    
    if log_details.user_type=="Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
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
                company=dash_details.company,
                login_details=log_details
            )
            items_data = request.POST.getlist('items')
            for item_data in items_data:
                item_id, custom_rate = map(int, item_data.split('-'))
                item = get_object_or_404(Items, id=item_id)
                PriceListItem.objects.create(
                    price_list=new_price_list,
                    item=item,
                    standard_rate=item.selling_price,
                    custom_rate=custom_rate,
                    company=dash_details.company,
                    login_details=log_details
                )

            return redirect('all_price_lists')
        context={
            'details':dash_details,
            
            'allmodules': allmodules,
        }
        return render(request,'zohomodules/price_list/create_price_list.html',context)
    

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
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        context={
            'details':dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'price_list': price_list,
        }
        return render(request,'zohomodules/price_list/price_list_details.html',context)
    
    if log_details.user_type=="Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details.company)
        price_list = get_object_or_404(PriceList, id=price_list_id)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        context={
            'details':dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'price_list': price_list,
        }
        return render(request,'zohomodules/price_list/price_list_details.html',context)
    


    # login_id = request.session.get('login_id')
    # price_list = get_object_or_404(PriceList, id=price_list_id)
    # price_list_items = PriceListItem.objects.filter(price_list=price_list)
    # transaction_history = PriceListTransactionHistory.objects.filter(price_list=price_list)

    # all_price_lists = PriceList.objects.filter(company=price_list.company)
    
    # log_details= LoginDetails.objects.get(id=login_id)
    # dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
    # allmodules= ZohoModules.objects.get(company=dash_details,status='New')

    # context = {
    #     'price_list': price_list,
    #     'price_list_items': price_list_items,
    #     'transaction_history': transaction_history,
    #     'all_price_lists': all_price_lists, 
    #     'allmodules': allmodules, 
        
    # }

    # return render(request, 'zohomodules/price_list/price_list_details.html', context)



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
            items_data = request.POST.getlist('items')
            for item_data in items_data:
                item_id, custom_rate = map(int, item_data.split('-'))
                item = get_object_or_404(Items, id=item_id)
                price_list_item, created = PriceListItem.objects.get_or_create(
                    price_list=price_list,
                    item=item,
                    company=dash_details,
                    login_details=log_details
                )
                if not created:
                    price_list_item.standard_rate = item.selling_price
                price_list_item.custom_rate = custom_rate
                price_list_item.save()
            return redirect('all_price_lists')
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'price_list': price_list,
        }
        return render(request, 'zohomodules/price_list/edit_price_list.html', context)
    elif log_details.user_type == "Staff":
        dash_details = StaffDetails.objects.get(login_details=log_details)
        price_lists = PriceList.objects.filter(company=dash_details.company)
        allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
        price_list = get_object_or_404(PriceList, id=price_list_id)
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'price_lists': price_lists,
            'price_list': price_list,
        }
        return render(request, 'zohomodules/price_list/edit_price_list.html', context)
    price_list = get_object_or_404(PriceList, id=price_list_id)
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
        items_data = request.POST.getlist('items')
        for item_data in items_data:
            item_id, custom_rate = map(int, item_data.split('-'))
            item = get_object_or_404(Items, id=item_id)
            price_list_item, created = PriceListItem.objects.get_or_create(
                price_list=price_list,
                item=item,
                company=dash_details,
                login_details=log_details
            )
            if not created:
                price_list_item.standard_rate = item.selling_price
            price_list_item.custom_rate = custom_rate
            price_list_item.save()
        return redirect('all_price_lists')

    context = {
        'details': dash_details,
        'price_list': price_list,
        'allmodules': allmodules,
    }
    return render(request, 'zohomodules/price_list/edit_price_list.html', context)



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


