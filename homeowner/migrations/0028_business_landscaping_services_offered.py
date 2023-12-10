# Generated by Django 4.2.7 on 2023-12-07 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeowner', '0027_remove_home_landscaping_service_needed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='landscaping_services_offered',
            field=models.CharField(blank=True, choices=[('lawn_mowing', 'Lawn Mowing'), ('tree_trimming', 'Tree Trimming'), ('lawn_care', 'Lawn Care')], max_length=255, null=True),
        ),
    ]