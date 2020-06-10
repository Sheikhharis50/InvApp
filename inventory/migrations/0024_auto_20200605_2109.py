# Generated by Django 3.0.5 on 2020-06-05 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_auto_20200603_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='item',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='contact',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
