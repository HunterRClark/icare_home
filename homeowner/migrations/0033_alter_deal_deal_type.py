# Generated by Django 4.2.7 on 2023-12-10 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeowner', '0032_alter_deal_deal_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='deal_type',
            field=models.CharField(choices=[('internet', 'Internet'), ('landscaping', 'Landscaping')], max_length=15),
        ),
    ]
