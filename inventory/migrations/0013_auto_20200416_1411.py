# Generated by Django 3.0.5 on 2020-04-16 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20200410_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='location',
            name='zipcode',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
