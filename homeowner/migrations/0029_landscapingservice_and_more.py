# Generated by Django 4.2.7 on 2023-12-07 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeowner', '0028_business_landscaping_services_offered'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandscapingService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(choices=[('lawn_mowing', 'Lawn Mowing'), ('tree_trimming', 'Tree Trimming'), ('lawn_care', 'Lawn Care')], max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='business',
            name='landscaping_services_offered',
        ),
        migrations.AddField(
            model_name='business',
            name='landscaping_services_offered',
            field=models.ManyToManyField(blank=True, to='homeowner.landscapingservice'),
        ),
    ]
