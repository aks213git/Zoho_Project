from django.urls import path
from . import views

urlpatterns = [
    # -------------------------------Company section--------------------------------
    path('Company-Dashboard',views.company_dashboard,name='company_dashboard'),
    path('Company-Profile',views.company_profile,name='company_profile'),
    path('Company/Staff-Request',views.company_staff_request,name='company_staff_request'),
    path('Company/Staff-Request/Accept/<int:pk>',views.staff_request_accept,name='staff_request_accept'),
    path('Company/Staff-Request/Reject/<int:pk>',views.staff_request_reject,name='staff_request_reject'),
    path('Company/All-Staffs',views.company_all_staff,name='company_all_staff'),
    path('Company/Staff-Approval/Cancel/<int:pk>',views.staff_approval_cancel,name='staff_approval_cancel'),




    # -------------------------------Staff section--------------------------------
    path('Staff-Dashboard',views.staff_dashboard,name='staff_dashboard'),
    path('Staff-Profile',views.staff_profile,name='staff_profile'),


    # -------------------------------Zoho Modules section--------------------------------
    
    
    #------------price lists-------------------
    path('all_price_lists', views.all_price_lists, name='all_price_lists'),
    path('create_price_list/', views.create_price_list, name='create_price_list'),
    path('price_list_details/<int:price_list_id>/', views.price_list_details, name='price_list_details'),
    path('edit_price_list/<int:price_list_id>/', views.edit_price_list, name='edit_price_list'),
    path('delete_price_list/<int:price_list_id>/', views.delete_price_list, name='delete_price_list'),
    path('toggle_price_list_status/<int:price_list_id>/', views.toggle_price_list_status, name='toggle_price_list_status'),
    
    path('add_pricelist_comment/<int:price_list_id>/', views.add_pricelist_comment, name='add_pricelist_comment'),
    path('delete_pricelist_comment/<int:comment_id>/<int:price_list_id>/', views.delete_pricelist_comment, name='delete_pricelist_comment'),
    
    path('email_pricelist/<int:price_list_id>/', views.email_pricelist, name='email_pricelist'),
    path('whatsapp_pricelist/<int:price_list_id>/', views.whatsapp_pricelist, name='whatsapp_pricelist'),
    path('price_list_pdf/<int:price_list_id>/', views.price_list_pdf, name='price_list_pdf'),
    path('attach_file/<int:price_list_id>/', views.attach_file, name='attach_file'),
    path('import_price_list/', views.import_price_list, name='import_price_list'),
    
]