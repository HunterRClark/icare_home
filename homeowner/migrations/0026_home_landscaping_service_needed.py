# Generated by Django 4.2.7 on 2023-12-07 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeowner', '0025_alter_home_internet_price_threshold'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='landscaping_service_needed',
            field=models.CharField(blank=True, choices=[('lawn_mowing', 'Lawn Mowing'), ('tree_trimming', 'Tree Trimming'), ('lawn_care', 'Lawn Care')], max_length=50, null=True),
        ),
    ]
