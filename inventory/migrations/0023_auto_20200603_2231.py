# Generated by Django 3.0.5 on 2020-06-03 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_auto_20200603_1822'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Vender',
            new_name='Vendor',
        ),
        migrations.RenameModel(
            old_name='Vender_Items',
            new_name='Vendor_Items',
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='vender',
            new_name='vendor',
        ),
        migrations.RenameField(
            model_name='vendor_items',
            old_name='vender',
            new_name='vendor',
        ),
    ]
