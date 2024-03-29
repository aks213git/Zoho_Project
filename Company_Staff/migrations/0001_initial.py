# Generated by Django 4.2.4 on 2024-01-09 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Register_Login', '0008_remove_zohomodules_reconciliation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(max_length=255)),
                ('item_name', models.CharField(max_length=255)),
                ('hsn_code', models.IntegerField(blank=True, null=True)),
                ('tax_reference', models.CharField(max_length=255, null=True)),
                ('intrastate_tax', models.IntegerField(blank=True, null=True)),
                ('interstate_tax', models.IntegerField(blank=True, null=True)),
                ('selling_price', models.IntegerField(blank=True, null=True)),
                ('sales_account', models.CharField(max_length=255)),
                ('sales_description', models.CharField(max_length=255)),
                ('purchase_price', models.IntegerField(blank=True, null=True)),
                ('purchase_account', models.CharField(max_length=255)),
                ('purchase_description', models.CharField(max_length=255)),
                ('minimum_stock_to_maintain', models.IntegerField(blank=True, null=True)),
                ('activation_tag', models.CharField(default='active', max_length=255)),
                ('inventory_account', models.CharField(max_length=255, null=True)),
                ('opening_stock', models.IntegerField(blank=True, default=0, null=True)),
                ('current_stock', models.IntegerField(blank=True, default=0, null=True)),
                ('opening_stock_per_unit', models.IntegerField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register_Login.companydetails')),
                ('login_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register_Login.logindetails')),
            ],
        ),
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('Sales', 'Sales'), ('Purchase', 'Purchase')], max_length=10)),
                ('item_rate_type', models.CharField(choices=[('Percentage', 'Percentage'), ('Each Item', 'Each Item')], max_length=15)),
                ('description', models.TextField()),
                ('percentage_type', models.CharField(blank=True, choices=[('Markup', 'Markup'), ('Markdown', 'Markdown')], max_length=10, null=True)),
                ('percentage_value', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('round_off', models.CharField(choices=[('Never Mind', 'Never Mind'), ('Nearest Whole Number', 'Nearest Whole Number'), ('0.99', '0.99'), ('0.50', '0.50'), ('0.49', '0.49')], max_length=20)),
                ('currency', models.CharField(choices=[('Indian Rupee', 'Indian Rupee')], max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register_Login.companydetails')),
                ('login_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register_Login.logindetails')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register_Login.companydetails')),
            ],
        ),
        migrations.CreateModel(
            name='PriceListTransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('action', models.CharField(choices=[('Created', 'Created'), ('Edited', 'Edited')], max_length=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register_Login.companydetails')),
                ('login_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register_Login.logindetails')),
                ('price_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Company_Staff.pricelist')),
            ],
        ),
        migrations.CreateModel(
            name='PriceListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('custom_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register_Login.companydetails')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Company_Staff.items')),
                ('login_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register_Login.logindetails')),
                ('price_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Company_Staff.pricelist')),
            ],
        ),
        migrations.AddField(
            model_name='items',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Company_Staff.unit'),
        ),
    ]
