# Generated by Django 4.2.7 on 2023-12-04 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeowner', '0010_profile_user_type_alter_profile_number_of_phones_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='business_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Business Name'),
        ),
    ]
