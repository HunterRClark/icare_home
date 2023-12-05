# Generated by Django 4.2.7 on 2023-12-04 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeowner', '0009_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('homeowner', 'Homeowner'), ('business', 'Business')], default='homeowner', max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='number_of_phones',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='Applicable for homeowners', null=True, verbose_name='Number of Phones'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_plan_contract_end_date',
            field=models.DateField(blank=True, help_text='Applicable for homeowners', null=True, verbose_name='Contract End Date'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_plan_cost',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Applicable for homeowners', max_digits=10, null=True, verbose_name='Monthly Cost'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_plan_data_limit',
            field=models.CharField(blank=True, help_text='Applicable for homeowners', max_length=255, null=True, verbose_name='Data Limit'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_plan_provider',
            field=models.CharField(blank=True, help_text='Applicable for homeowners', max_length=255, null=True, verbose_name='Phone Plan Provider'),
        ),
    ]
