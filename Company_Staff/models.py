from django.db import models

# Create your models here.

#---------------- models for zoho modules--------------------

from Register_Login.models import *

#------------------- items module ------------
class Unit(models.Model):
    
    unit_name=models.CharField(max_length=255)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)

class Items(models.Model):
   
    item_type=models.CharField(max_length=255)
    item_name=models.CharField(max_length=255)
   
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE)
    hsn_code=models.IntegerField(null=True,blank=True)
    tax_reference=models.CharField(max_length=255,null=True)
    intrastate_tax=models.IntegerField(null=True,blank=True)
    interstate_tax=models.IntegerField(null=True,blank=True)

    selling_price=models.IntegerField(null=True,blank=True)
    sales_account=models.CharField(max_length=255)
    sales_description=models.CharField(max_length=255)

    purchase_price=models.IntegerField(null=True,blank=True)
    purchase_account=models.CharField(max_length=255)
    purchase_description=models.CharField(max_length=255)
   
    minimum_stock_to_maintain=models.IntegerField(blank=True,null=True)  
    activation_tag=models.CharField(max_length=255,default='active')
    inventory_account=models.CharField(max_length=255,null=True)

   
    opening_stock=models.IntegerField(blank=True,null=True,default=0)
    current_stock=models.IntegerField(blank=True,null=True,default=0)
    opening_stock_per_unit=models.IntegerField(blank=True,null=True,)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE)


#------------------- PRICE LIST MODULE ------------

class PriceList(models.Model):
    
    name = models.CharField(max_length=255, null=True)
    type_choices = [
        ('Sales', 'Sales'),('Purchase', 'Purchase'),]
    type = models.CharField(max_length=10, choices=type_choices, null=True)
    item_rate_choices = [('Percentage', 'Percentage'),('Each Item', 'Each Item'),]
    item_rate_type = models.CharField(max_length=15, choices=item_rate_choices, null=True)
    description = models.TextField(null=True)
    percentage_type_choices = [('Markup', 'Markup'),('Markdown', 'Markdown'),]
    percentage_type = models.CharField(max_length=10, choices=percentage_type_choices, null=True, blank=True)
    percentage_value = models.IntegerField(null=True, blank=True)
    round_off_choices = [
        ('Never Mind', 'Never Mind'),
        ('Nearest Whole Number', 'Nearest Whole Number'),
        ('0.99', '0.99'),
        ('0.50', '0.50'),
        ('0.49', '0.49'),
    ]
    round_off = models.CharField(max_length=20, choices=round_off_choices, null=True)
    currency_choices = [('Indian Rupee', 'Indian Rupee')]
    currency = models.CharField(max_length=20, choices=currency_choices, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    STATUS_CHOICES = [('Active', 'Active'),('Inactive', 'Inactive'),]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    attachment = models.FileField(upload_to='price_list_attachment/', null=True, blank=True)

    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE)

class PriceListItem(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE)
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)  
    standard_rate = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    custom_rate = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

class PriceListTransactionHistory(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE)
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True,null=True)
    action_choices = [
        ('Created', 'Created'), 
        ('Edited', 'Edited')
        ]
    action = models.CharField(max_length=10, choices=action_choices,null=True)

class PriceListComment(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE)
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

